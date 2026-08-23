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

## Author
Rashi Sharma