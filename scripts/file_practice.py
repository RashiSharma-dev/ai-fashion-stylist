import json

# ---- Part 1: Basic file writing ----
with open("data/hello.txt", "w") as f:
    f.write("hello")

print("hello.txt created!")

# ---- Part 2: Create a color profile dictionary ----
color_profile = {
    "skin_tone": "warm",
    "recommended": ["blue", "green", "camel"]
}

# ---- Part 3: Save (write) this dictionary as a JSON file ----
def save_profile(profile, filename):
    with open(filename, "w") as f:
        json.dump(profile, f)
    print(f"Saved profile to {filename}")

# ---- Part 4: Load (read) the JSON file back ----
def load_profile(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# Save it
save_profile(color_profile, "data/color_profile.json")

# Load it back
loaded_data = load_profile("data/color_profile.json")
print("Loaded profile:", loaded_data)
print("Skin tone from loaded data:", loaded_data["skin_tone"])
