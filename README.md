
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
