# AI Fashion Color Fit Matcher & Virtual Stylist

An AI-powered Streamlit app that detects your skin tone from a photo,
recommends clothing colors, suggests full outfits, and lets you preview
outfit colors on yourself with a virtual try-on overlay.

## Features

### Skin Tone Analysis
- Face detection using OpenCV Haar Cascade
- HSV-based skin tone classification (warm / cool / neutral)
- Personalized color palette recommendations from a rules-based engine

### Outfit Color Extraction
- K-Means clustering to extract dominant colors from any clothing photo
- Visual color palette strip with HEX codes

### Outfit Compatibility Checker
- Combines skin tone detection + dominant color extraction
- Instant compatibility verdict (✓ Excellent / ✗ Not Ideal)

### Color Harmony Engine
- Complementary and analogous color pair detection using Euclidean
  distance in RGB space, based on color wheel theory

### Outfit Recommendation Engine
- 150-row outfit database with cascading fallback matching
  (exact → season-relaxed → color-only)
- Explainable recommendations — every result shows *why* it was chosen
- Real-time weighted match scoring (skin match + color harmony +
  occasion fit)
- Live sidebar filters (skin tone, occasion, season, gender, style)

### Live Webcam Features
- Real-time face detection with FPS counter
- Real-time skin tone classification (throttled for performance)
- One-click "Analyze My Look" pipeline with browser-based camera capture

### Virtual Try-On
- Alpha-blended color overlay restricted to the estimated torso region
- Live color picker with adjustable overlay strength
- Connected directly to outfit recommendations — preview any
  recommended outfit's color on your own photo

### User Profiles & Reports
- Session-based + JSON-persisted user profiles (remembers returning
  users' last search)
- Downloadable HTML style report with top recommendations

### Robust Error Handling
- Graceful handling of no-face, low-brightness, and invalid file inputs
  across the entire app

## Tech Stack
- Python 3.11.9
- OpenCV (face detection, image processing)
- scikit-learn (K-Means clustering)
- Streamlit (web app framework)
- Pandas / NumPy (data handling)
- Pillow (image handling)

## Screenshots
See `docs/screenshots/` for a visual walkthrough of key features.

## Project Status
v0.2 — Core features complete (Phase 2: AI Core Features, Phase 3
early progress: Webcam + Virtual Try-On). See `docs/` for architecture
diagrams, data flow documentation, and the demo script.

## 💬 AI Stylist Chatbot

An AI-powered conversational stylist, built with Groq's `openai/gpt-oss-20b`
model, that gives personalized fashion advice grounded in the user's own
skin tone analysis.

### Key Features
- **Context-aware**: automatically knows the user's detected skin tone and
  selected occasion — no need to repeat that information in every message.
- **Auto-personalized greeting**: the moment a user finishes an analysis
  and opens the chat, the AI proactively summarizes their results and
  offers quick styling tips — no user input required to start.
- **Conversation memory**: the full chat history is resent with every
  request, so the AI maintains context across multiple turns.
- **Scope-limited & safe**: the chatbot is restricted to fashion and
  styling topics via a dedicated system prompt rule, with graceful
  redirects for off-topic questions and a warmer, non-dismissive
  response if a user expresses distress.

### Example Conversation

> **AI Stylist:** Hi there! Based on your analysis, you have a warm skin
> tone — gorgeous! A few quick tips: earthy tones like olive and rust
> will really make your complexion pop, and warm gold jewelry beats
> silver for you every time.
>
> **You:** What about accessories for a formal look?
>
> **AI Stylist:** For a formal look that flatters a warm skin tone, go for gold‑tinted accessories: a classic gold watch, rose‑gold cufflinks, and a gold tie clip. Pair those with a crisp, deep‑burgundy or camel pocket square to echo the warm undertones. Choose leather shoes and belt in a rich brown (not black) to keep the ensemble cohesive. Add a sleek, black or deep‑navy clutch for a touch of contrast that still feels polished. Keep the overall palette muted and sophisticated, letting the warm accents pop subtly.
>
> **You:** What's the score of today's cricket match?
>
> **AI Stylist:** I’m a fashion stylist! Ask me about colors, outfits, or style tips

### Tech Stack
`Groq API` · `openai/gpt-oss-20b` · `python-dotenv` (secure key storage) ·
Streamlit `st.chat_message` / `st.chat_input`

## 🔭 Future Scope

- **Automated body shape detection**: Currently, body shape is self-selected
  by the user via a dropdown. Reliable automated detection would require
  full-body pose estimation and is sensitive to camera angle and clothing —
  a substantial computer vision project on its own, intentionally out of
  scope for this version.

## Author
Rashi Sharma