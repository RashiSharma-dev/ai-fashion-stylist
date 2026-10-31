# Live Demo Script

Main demo: about 7 minutes. Optional segments below can be swapped in or out.
Do NOT refresh the browser during the main demo, because the app remembers your quiz and analysis only while the same tab stays open.

## Before you start (10 minutes before)

- Open the live app link and click to the Home page, so the server is awake
- Start the local backup: terminal with (venv), then streamlit run app.py
- Turn on the phone hotspot, ready as a backup for WiFi
- Laptop charged, charger plugged in
- Close other apps, so the camera is free for the browser
- Test photos on the desktop: one clear front-facing selfie, one clothing photo, one photo with no face
- Zoom the browser to 110 percent so the back row can read it

## Main demo: 7 steps

| # | Time | Page | What to click | What to say (short) | If it fails |
|---|---|---|---|---|---|
| 1 | 0:00 | Home | Show the page | "This is our AI Fashion Color Fit Matcher. It finds your skin tone from a photo and recommends colors and outfits that suit you, using computer vision and machine learning in a Streamlit web app." | Say the sentence, move on |
| 2 | 0:40 | Style Quiz | Answer the 5 questions, show the persona result | "First, a 5-question quiz gives a style personality. The app uses it later to personalize advice." | Skip to step 3 and mention the quiz verbally |
| 3 | 1:40 | Analyze My Look | Pick an occasion, season and body shape. Take a photo with the camera. Click Analyze. | "Now the main feature. OpenCV's Haar cascade finds the face, we average the Hue and Saturation in HSV color space, and simple rules decide warm, neutral or cool. Here it says [say the real result]." | Camera blocked: use the upload box with the saved selfie |
| 4 | 3:00 | Analyze results | Scroll through the skin tone, the style advice and the outfit cards. Open one "Why this outfit?" | "Each outfit is scored: 40 percent skin match, 30 percent color harmony, 30 percent occasion fit. Every score comes from a visible rule, so we can always explain why an outfit was chosen." | If no outfits appear, change the occasion or season |
| 5 | 4:00 | Virtual Try-On | Choose a color and apply it | "This previews a color on your own photo, using alpha blending on the estimated torso." | Skip, and mention it as a limitation |
| 6 | 4:50 | AI Stylist Chat | Read the greeting. Ask "What should I wear to a party?" Then ask "Who won the cricket match?" | "The chatbot uses Groq and knows my skin tone, occasion and quiz result. It stays on fashion and politely declines other topics." | If it says "Offline mode", say: "This is our fallback when the AI service is unreachable. The app still gives advice from its own rules." |
| 7 | 6:00 | Dashboard | Open the bar chart tab, then the pie chart tab | "The dashboard counts photos analyzed, outfits viewed and chat messages." | Skip |

## Optional segments (from the earlier script)

Add one or two if you have time. To make room, drop step 5 or 7 first.

| Segment | Time | Page | What to click | What to say | If it fails |
|---|---|---|---|---|---|
| A. Upload and Result | 1 min | Upload, then Result | Upload a selfie, then open Result | "This is the same skin tone analysis through a simple upload. The app then recommends a color palette from a rules file, not a black box." | Skip |
| B. Clothing colors | 1 min | Outfit Colors | Upload a clothing photo | "Any clothing photo can be analyzed. K-Means clustering groups the pixels by color and extracts the 5 most dominant colors, shown as a palette with HEX codes." | Skip |
| C. Outfit Match | 45 sec | Outfit Match | Upload a selfie and an outfit photo | "This combines both features. It checks whether the outfit's dominant color suits my detected skin tone and gives a clear verdict." | Skip |
| D. Filters | 1 min | Recommendations | Type a name in the sidebar and change Occasion, Season, Gender and Style | "We filter a database of 150 outfits by the skin tone's recommended colors, occasion and season. A cascading fallback means there is always a result, even for narrow searches. The bar shows the match score." | Change the filters back to the defaults |
| E. Returning user (risky) | 30 sec | Recommendations | Type the same name as before, only AFTER everything else | "The app remembers returning users with lightweight JSON files, so no database is needed at this stage." | If nothing is shown, say: "Profiles are saved in a local file, so they may reset on the hosted server." Don't use this segment on the live link if the profile did not save in your rehearsal. |

Use a name nobody else would use, because profiles are shared between visitors on the hosted app.

## Closing line (15 seconds)

"To summarize: it is live, tested with 12 automated tests, and it still works if the AI service or the internet fails. Thank you. We are happy to take questions."

## If something goes wrong (the 4 rules)

1. Stay calm and say what happened in one short sentence, for example: "The camera is blocked, so I will use the upload option."
2. WiFi down: switch the laptop to the phone hotspot. If that fails, open the local backup at http://localhost:8501. The chat will show its offline replies, which is itself a feature.
3. Page error: refresh once, then move to the next step. Don't debug on stage.
4. Never say "this worked yesterday". Say what the backup is and continue.

## Questions during the demo

- "How accurate is it?" Say: "We have not benchmarked it on a labeled photo set yet, so I can't give a percentage. It uses fixed thresholds, so lighting matters."
- "Why rules instead of deep learning?" Say: "No labeled dataset or GPU, and rules are instant and explainable."
- "Is my photo stored?" Say: "It is saved to a temporary file that the next photo overwrites. On the hosted version, a fix is unique file names."
