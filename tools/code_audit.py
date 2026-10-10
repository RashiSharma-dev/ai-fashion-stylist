"""
Code audit tool (Day 78).

Scans every .py file in the project and reports:
  1. Functions, methods, and classes that have no docstring
  2. print() calls (possible leftover debugging)
  3. Commented-out code (heuristic: comment text that is valid Python)
  4. Vague variable names (x, temp, data1, stuff, ...)

Not reported (on purpose):
  - Anything inside the "scripts" folder (practice and one-off scripts)
  - print() inside `if __name__ == "__main__":` blocks (self-test demos)
  - print() in files named test_*, generate_*, or verify_* (they exist to print)
  - Comments that are just a file path, like "# src/chatbot.py"

Run it from the project root:
    python tools/code_audit.py
"""
import ast
import os
import re

# Folders we never scan (libraries, generated files, and non-app scripts)
SKIP_DIRS = {"venv", ".venv", "__pycache__", ".git", "node_modules", "scripts"}

# Files whose whole purpose is to print, so print() is fine there
PRINT_OK_PREFIXES = ("test_", "generate_", "verify_")

# Variable names that tell the reader nothing
VAGUE_NAMES = {"x", "temp", "tmp", "data1", "data2", "stuff", "thing", "foo", "bar", "asdf"}


def find_python_files(root):
    """Yield the path of every .py file under root, skipping library folders and this tool."""
    this_file = os.path.abspath(__file__)
    for folder, subfolders, filenames in os.walk(root):
        subfolders[:] = [name for name in subfolders if name not in SKIP_DIRS]
        for filename in filenames:
            path = os.path.join(folder, filename)
            if filename.endswith(".py") and os.path.abspath(path) != this_file:
                yield path


def find_missing_docstrings(tree):
    """Return (line, kind, name) for every function, method, or class without a docstring."""
    problems = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "function"
        elif isinstance(node, ast.ClassDef):
            kind = "class"
        else:
            continue
        if ast.get_docstring(node) is None:
            problems.append((node.lineno, kind, node.name))
    return problems


def main_guard_lines(tree):
    """Return the line numbers inside `if __name__ == "__main__":` blocks."""
    lines = set()
    for node in tree.body:
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
        ):
            lines.update(range(node.lineno, node.end_lineno + 1))
    return lines


def find_print_calls(tree):
    """Return the line number of every print(...) call outside `if __name__ == "__main__":` blocks."""
    ignored = main_guard_lines(tree)
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
        and node.lineno not in ignored
    ]


def find_vague_names(tree):
    """Return (line, name) for every vague variable or parameter name."""
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in VAGUE_NAMES:
            found.add((node.lineno, node.id))
        elif isinstance(node, ast.arg) and node.arg in VAGUE_NAMES:
            found.add((node.lineno, node.arg))
    return sorted(found)


def looks_like_code(text):
    """Return True if a comment's text looks like a line of Python code."""
    # A bare file path like "src/chatbot.py" is a label, not code
    if re.fullmatch(r"[\w./\\-]+\.py", text):
        return False

    candidates = [text]
    if text.endswith(":"):
        candidates.append(text + " pass")  # lets "if x:" or "for a in b:" parse

    for candidate in candidates:
        try:
            parsed = ast.parse(candidate)
        except SyntaxError:
            continue
        if not parsed.body:
            continue
        # Plain words ("TODO") and labels ("Note: ...") are normal comments, not code
        is_plain_comment = any(
            (isinstance(stmt, ast.Expr) and isinstance(stmt.value, (ast.Name, ast.Constant)))
            or isinstance(stmt, ast.AnnAssign)
            for stmt in parsed.body
        )
        if not is_plain_comment:
            return True
    return False


def find_commented_code(lines):
    """Return (line, text) for every comment line that looks like commented-out code."""
    found = []
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("#!"):
            content = stripped.lstrip("#").strip()
            if content and looks_like_code(content):
                found.append((number, stripped))
    return found


def safe(text):
    """Make text safe to print on any Windows console (replaces emoji and odd characters)."""
    return text.encode("ascii", "replace").decode("ascii")


def audit_file(path):
    """Return a list of (line, message) problems for one file, plus a dict of counts."""
    with open(path, "r", encoding="utf-8", errors="replace") as file:
        source = file.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        return [(error.lineno or 0, f"cannot parse file: {error.msg}")], {"parse": 1}

    problems = []
    counts = {"docstring": 0, "print": 0, "commented": 0, "vague": 0}

    for line, kind, name in find_missing_docstrings(tree):
        problems.append((line, f"missing docstring: {kind} {name}"))
        counts["docstring"] += 1

    if not os.path.basename(path).startswith(PRINT_OK_PREFIXES):
        for line in find_print_calls(tree):
            problems.append((line, "print() call"))
            counts["print"] += 1

    for line, text in find_commented_code(source.splitlines()):
        problems.append((line, f"commented-out code: {safe(text)}"))
        counts["commented"] += 1
    for line, name in find_vague_names(tree):
        problems.append((line, f"vague name: {name}"))
        counts["vague"] += 1

    return sorted(problems), counts


def main():
    """Scan the whole project and print a report."""
    root = os.getcwd()
    totals = {"docstring": 0, "print": 0, "commented": 0, "vague": 0, "parse": 0}
    files_scanned = 0

    for path in sorted(find_python_files(root)):
        files_scanned += 1
        problems, counts = audit_file(path)
        for key, value in counts.items():
            totals[key] += value
        if problems:
            print(os.path.relpath(path, root))
            for line, message in problems:
                print(f"  line {line:<4} {message}")
            print()

    print("=" * 50)
    print(f"Files scanned:          {files_scanned}")
    print(f"Missing docstrings:     {totals['docstring']}")
    print(f"print() calls:          {totals['print']}")
    print(f"Commented-out code:     {totals['commented']}")
    print(f"Vague variable names:   {totals['vague']}")
    if totals["parse"]:
        print(f"Files that won't parse: {totals['parse']}")
    if sum(totals.values()) == 0:
        print("All clear!")


if __name__ == "__main__":
    main()
