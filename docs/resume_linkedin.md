# Resume and LinkedIn Text

## 1. Resume: project entry 

**AI Fashion Color Fit Matcher & Virtual Stylist** | Python, Streamlit, OpenCV, scikit-learn, Groq API
Live app: https://ai-fashion-stylist.streamlit.app/ | Code: https://github.com/RashiSharma-dev/ai-fashion-stylist

- Built a 13-page web app that detects a face, classifies skin tone (warm, neutral, cool) from average HSV values, and recommends colors and outfits ranked by an explainable score (40% skin match, 30% color harmony, 30% occasion fit).
- Extracted dominant clothing colors with K-Means clustering; cut photo processing from 2-3 minutes to seconds by resizing images, and cut K-Means time from about 3,100 ms to 230 ms in a speed test by reducing restarts.
- Integrated a Groq-powered AI stylist chatbot with a fashion-only scope, a 15-second timeout, and an offline fallback so the app keeps working when the AI service or internet fails.
- Wrote 14 pytest tests, found and fixed a hue wrap-around bug in the skin tone averaging, and deployed the app on Streamlit Community Cloud with the API key kept in secrets.

## 2. Resume: short version 

**AI Fashion Color Fit Matcher & Virtual Stylist** | Python, OpenCV, scikit-learn, Streamlit
- Built and deployed a 13-page web app that classifies skin tone from a photo using OpenCV and HSV rules, and ranks outfits with an explainable 40/30/30 score.
- Added K-Means color extraction, a Groq AI chatbot with offline fallback, and 14 pytest tests; live on Streamlit Cloud.

## 3. Resume: skills line

Python, OpenCV, scikit-learn (K-Means), Streamlit, pandas, NumPy, Groq API (LLM), pytest, Git and GitHub, Streamlit Community Cloud

## 4. LinkedIn post

I just deployed my final-year project: an AI Fashion Color Fit Matcher and Virtual Stylist 🎨

You upload a photo. It finds your face, classifies your skin tone as warm, neutral or cool, and recommends colors and outfits that suit you, with a score you can explain instead of a black box.

What's inside:
• Face detection (OpenCV) and HSV skin tone rules
• K-Means clustering for clothing colors
• Outfit scoring: 40% skin match, 30% color harmony, 30% occasion fit
• An AI stylist chatbot (Groq) with an offline fallback
• 13 pages, 14 automated tests, live on Streamlit Cloud

Three things I learned:
1. Measure before you optimize. A 2-3 minute upload became seconds.
2. Test your assumptions. I found that OpenCV's hue wraps around, which can flip a skin tone result, and fixed it.
3. Plan for failure. The app still answers when the AI service is down.

It has limits: the rules are simple and I have not yet measured accuracy on a labeled photo set. That is my next step.

Try it: https://ai-fashion-stylist.streamlit.app/
Code: https://github.com/RashiSharma-dev/ai-fashion-stylist

#Python #ComputerVision #MachineLearning #Streamlit #OpenCV

## 5. GitHub "About" line 

AI app that classifies skin tone from a photo and recommends flattering colors and outfits, with an AI stylist chatbot. Python, OpenCV, Streamlit.

## 6. LinkedIn "Projects" description 

Web app that finds your face, classifies skin tone with OpenCV and HSV rules, and ranks outfits with an explainable score. Includes K-Means color extraction, a Groq AI chatbot with offline fallback, 14 tests, and a live deployment.
