
# AI Fashion Color Fit Matcher & Virtual Stylist

An AI-powered app that detects skin tone from a photo and recommends 
the best clothing colors and outfits, with a chatbot stylist for 
personalized fashion advice.

## Features
- Skin tone detection
- Color recommendations
- Outfit suggestions
- AI chatbot stylist

# ai-fashion-stylist
 "AI Fashion Color Fit Matcher &amp; Virtual Stylist"
## System Architecture

The app is built with 5 main components:
1. **UI (Streamlit)** - handles user interaction, photo upload, and displaying results
2. **Color Engine** - detects skin tone and extracts dominant colors from images using OpenCV
3. **Outfit Matcher** - matches detected colors with suitable outfits from the database
4. **Chatbot** - AI-powered fashion assistant that answers styling questions
5. **Database** - stores outfit data, color rules, and user profiles (CSV/JSON files)

See `docs/architecture-sketch.jpg` for the visual diagramss.

## Technologies Used

- **Python** - main programming language
- **OpenCV (cv2)** - image loading, processing, and color space conversion
- **NumPy** - array/matrix operations (images are represented as arrays)
- **Pillow (PIL)** - creating and saving images
- **Pandas** - managing the outfit database (CSV data)
- **Matplotlib** - creating charts and visualizations
- **JSON** - storing structured data like color profiles and rules

## Current UI Status

The app now has 3 working pages: Home, Upload, and Results, with 
working navigation and shared data between pages using session_state.

**What looks good:**
- Dark theme with pink accents feels cohesive
- Navigation between pages works smoothly
- Photo upload and preview works reliably

**What to improve later:**
- Add more visual polish to results page (currently just shows photo)
- Add loading states when processing
- Improve mobile responsiveness