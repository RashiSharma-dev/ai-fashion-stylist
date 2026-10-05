# AI Fashion Color Fit Matcher & Virtual Stylist: Feature Inventory

**Label key:**
- **MVP**: the project doesn't work without it
- **Advanced**: makes the project stand out
- **Optional**: polish or nice-to-have

## 30-Second Summary

The AI Fashion Color Fit Matcher is a Streamlit web app that detects your skin tone from a photo, recommends outfit colors and full outfits that suit you, lets you virtually try colors on your own photo, and includes an AI Stylist chatbot that gives personalized advice based on your skin tone, occasion, body shape, and style personality.

## 1. Core AI Pipeline

| Feature | Description | Label | Main files |
|---|---|---|---|
| Photo upload | Lets the user upload a selfie from their device for analysis. | MVP | `pages/2_Upload.py` |
| Face detection | Finds the face in a photo using OpenCV so the skin region can be analyzed. | MVP | `src/color_recommender.py` |
| Skin tone classification | Classifies the detected face into a skin tone category. | MVP | `pages/3_Result.py`, `src/color_recommender.py` |
| Dominant color extraction | Uses K-Means clustering to find the main colors in an image. | MVP | `src/dominant_color_extractor.py` |
| Palette visualization | Draws the extracted dominant colors as a clean color palette. | MVP | `src/palette_generator.py` |
| Color harmony checker | Checks whether two colors look good together using color-theory rules. | MVP | `src/color_harmony.py` |
| Outfit compatibility check | Compares the outfit's colors against the user's skin tone from selfie and outfit photos. | MVP | `src/outfit_compatibility.py`, `pages/5_Outfit_Match.py` |
| Outfit color extraction | Pulls the main colors out of an outfit photo. | MVP | `pages/4_Outfit_Colors.py` |
| Input validation and error handling | Catches bad or missing photos and returns friendly error messages instead of crashing. | MVP | `src/image_validation.py` |

## 2. Recommendation Engine

| Feature | Description | Label | Main files |
|---|---|---|---|
| Color rules database | Stores which colors suit which skin tones in a JSON file. | MVP | `data/color_rules.json` |
| Outfit database | Holds 150 outfit combinations tagged by skin tone, occasion, season, gender, and style. | MVP | `src/generate_outfits.py` |
| Outfit recommender | Picks the best outfits for a user, with cascading fallback rules so results are never empty. | MVP | `src/recommender.py`, `data/recommendation_rules.json` |
| Weighted match score | Scores every outfit using 40% skin match, 30% color harmony, and 30% occasion fit. | MVP | `src/recommender.py` |
| "Why this outfit?" explanations | Explains in plain English why an outfit was recommended. | Advanced | `src/recommender.py` (`explain()`) |
| Recommendations page with filters | Shows styled outfit cards with sidebar filters for skin tone, occasion, season, gender, and style. | MVP | `pages/6_Recommendations.py` |

## 3. One-Click Experience

| Feature | Description | Label | Main files |
|---|---|---|---|
| Analyze My Look | Runs the whole pipeline (photo, skin tone, outfits, advice) from a single button. | MVP | `pages/8_Analyze_My_Look.py` |
| Webcam capture | Takes a photo directly with the device camera. | Advanced | `pages/7_Webcam_Capture.py` |
| Real-time face detection | Shows live face detection with an FPS counter and a throttled skin tone readout. | Optional | `pages/7_Webcam_Capture.py` |
| User profile save/load | Saves a user's results so they can be loaded again later. | Advanced | `src/user_profile.py` |
| Downloadable style report | Exports the user's results as an HTML report. | Advanced | `src/report_generator.py` |

| Mirror Mode | A full-screen "smart mirror" page with a camera, live outfit cards, and a built-in stylist chat. | Advanced | `pages/13_Mirror_Mode.py` |

## 4. Virtual Try-On

| Feature | Description | Label | Main files |
|---|---|---|---|
| Color overlay | Blends a chosen color onto a photo using alpha blending. | Advanced | `src/color_overlay.py` |
| Torso-only overlay | Limits the color change to the torso area so the face and background stay untouched. | Advanced | `src/torso_overlay.py` |
| Live color picker and strength slider | Lets the user pick any color and control how strong the effect is. | Advanced | `pages/9_Virtual_TryOn.py` |
| "Preview on My Photo" buttons | Applies a recommended outfit color to the user's photo in one click. | Advanced | `pages/9_Virtual_TryOn.py` |

## 5. AI Stylist Chatbot

| Feature | Description | Label | Main files |
|---|---|---|---|
| Groq-powered chatbot | Answers fashion questions using a large language model through the Groq API. | Advanced | `src/chatbot.py` |
| Context-aware replies | Uses the user's skin tone, occasion, body shape, and style personality in every answer. | Advanced | `src/chatbot.py` (`build_system_prompt`) |
| Conversation memory | Remembers the whole chat during a session. | Advanced | `st.session_state.chat_messages` |
| Personalized greeting | Greets the user automatically with their analysis results. | Advanced | `src/chatbot.py` (`get_greeting_reply`) |
| Scope limiting | Keeps the bot on fashion topics and redirects politely when asked about anything else. | Advanced | `src/chatbot.py`, `docs/chatbot_scope_test_results.txt` |
| Styled chat bubbles | Shows chat messages in pink/dark themed bubbles. | Optional | `pages/10_AI_Stylist_Chat.py` |
| Typing-dots animation | Shows a "typing" animation while the bot is thinking. | Optional | `pages/10_AI_Stylist_Chat.py` |
| Quick-reply buttons | Gives one-tap suggested questions. | Optional | `pages/10_AI_Stylist_Chat.py` |

## 6. Style Intelligence (Week 10)

| Feature | Description | Label | Main files |
|---|---|---|---|
| Seasonal palettes | Suggests colors, fabrics, and patterns for the current season. | Advanced | `src/seasonal_colors.py`, `data/seasonal_palettes.json` |
| Occasion advisor | Gives DO/DON'T color guidance for six occasions. | Advanced | `src/occasion_advisor.py`, `data/occasion_rules.json` |
| Icon-button occasion selector | Lets the user pick an occasion with styled buttons instead of a dropdown. | Optional | `pages/8_Analyze_My_Look.py` |
| Body shape advisor | Gives fit advice for five self-selected body shapes. | Advanced | `src/body_shape_advisor.py`, `data/body_shape_rules.json` |
| Combined style advice | Merges skin tone, occasion, body shape, and style persona into one piece of advice. | Advanced | `src/style_advisor.py` |
| Trending colors | Shows real Pantone Colors of the Year and checks if a trend suits the user. | Advanced | `src/trending_colors.py`, `data/trending_colors.json` |
| Style personality quiz | Asks 5 questions and assigns one of three personas: Classic Minimalist, Bold Maximalist, or Boho Chic. | Advanced | `src/style_quiz.py`, `pages/11_Style_Quiz.py` |

## 7. Analytics

| Feature | Description | Label | Main files |
|---|---|---|---|
| Activity tracking | Counts photos analyzed, outfits viewed, and chatbot messages, and saves them between sessions. | Advanced | `src/analytics.py` |
| Dashboard | Shows session stats, a "most recommended colors" bar chart, and an "occasions styled" pie chart. | Advanced | `pages/12_Dashboard.py` |

## 8. Interface and Infrastructure

| Feature | Description | Label | Main files |
|---|---|---|---|
| Multi-page Streamlit app | Splits the app into separate pages with sidebar navigation. | MVP | `app.py`, `pages/` |
| Custom pink/dark theme | Applies a consistent brand look across every page. | Optional | `.streamlit/config.toml` |
| Home page | Introduces the app and shows trending colors. | MVP | `pages/1_Home.py` |
| Secure API key handling | Keeps the Groq key in a gitignored `.env` file so it never reaches GitHub. | MVP | `.env`, `.gitignore` |

## Known Limitations and Future Scope

- Body shape is **self-selected**, not auto-detected, because reliable detection needs full-body pose estimation.
- The recommendation database is limited to 150 outfits.
- Skin tone detection works best in even lighting.
- Mirror Mode uses single-photo capture; continuous live video would need `streamlit-webrtc`.
