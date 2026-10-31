# Interview and Viva Prep: AI Fashion Color Fit Matcher & Virtual Stylist

Rule for every answer: problem, what I did, result with a number. Say it in your own words.

## Part 1: Questions about YOU

**Q1. Tell me about your project (30 seconds).**
We built a web app that finds your face in a photo, classifies your skin tone as warm, neutral or cool, and recommends colors and ranked outfits that suit you. It also has a color try-on preview, a style quiz, and an AI stylist chatbot. It is deployed live on Streamlit Cloud, has 13 pages and 12 automated tests, and every recommendation can be explained by a visible rule.

**Q2. What was your role?**
I was the primary developer. I built the application end to end: the face detection and skin tone logic, the color extraction with K-Means, the outfit recommender and its scoring, the AI chatbot, the 13 Streamlit pages and the UI theme, the automated tests, the deployment, and the documentation. That is why I can open any file and explain it line by line.

**Q3. What was the hardest challenge?**
Photo analysis took 2 to 3 minutes on the Outfit Colors page. K-Means ran on the full-resolution phone photo, with 10 random restarts. I added a function that shrinks every image to at most 300 pixels before clustering, and processing dropped to seconds. Later, profiling showed K-Means was still our slowest step, so I cut the restarts from 10 to 3, and in a speed test it went from about 3,100 ms to about 230 ms.

**Q4. Tell me about a bug you found and fixed.**
Our functions returned `None` for some failures and a dictionary for success, so every page needed different checks, and one check crashed when a selfie had no face. I rewrote the functions to always return a dictionary with an `error` field (empty on success, a friendly message on failure), and updated every page to check `result.get("error")`. I also added an image validation module for dark or unreadable photos.

**Q5. Tell me about another problem.**
Two examples. (1) The chatbot showed duplicate messages, because each message was both displayed directly and saved to the history. I made the history loop the only place messages are displayed. (2) Our Groq model was retired twice without warning, so the chatbot suddenly failed. I learned to handle API errors with a friendly fallback and to check the available models when an error mentions the model.

**Q6. What did you learn?**
Three things. First, measure before you optimize: our upload page took minutes, profiling showed K-Means was the slow step, and shrinking images and cutting restarts took it from about 3,100 ms to about 230 ms. Second, plan for failure: every function returns a clear error instead of crashing, and the chatbot has an offline fallback. Third, never put secrets on GitHub: the API key stays in a gitignored file and Cloud secrets.

**Q7. What would you do differently?**
I'd measure skin tone accuracy on a labeled photo set from the start, and collect real outfit data instead of generating it. I'd also write tests earlier, because we only added them near the end.

**Q8. You said you started with little coding experience. How did you build this?**
I followed a daily plan, one small feature at a time, with a Git commit every day. Each day I built something that ran, tested it, and moved on. After about 87 days that added up to the whole system. Say this honestly. It is a strength.

**Q9. Did you use AI tools?**
Yes, I used an AI assistant as a tutor to explain steps and review errors. I typed, ran, tested and debugged the code myself.

**Q10. What are you most proud of?**
Choose one and give a fact: the app is live and handles failure (it still works with no internet, using offline replies and a photo upload backup), or the scoring is fully explainable (40% skin match, 30% harmony, 30% occasion fit).

**Q11. How did your team work together?**
I took ownership of the implementation and drove it with a daily plan and a Git commit every day, so the whole history is in one GitHub repository. My teammates did the testing, deployment and other works for implementing the project such as giving feedback on the design, testing the app and helping with the presentation.

## Part 2: Technical questions

**Q12. How does skin tone detection work?**
A Haar cascade finds the face. The face pixels are converted to HSV and averaged. Hue of 20 or less with saturation above 60 is warm. Hue of 20 or less with saturation of 60 or below is neutral. Hue above 20 is cool.

**Q13. Why HSV and not RGB?**
HSV separates color (hue) from brightness, so the rule is less sensitive to how bright the photo is.

**Q14. How do you use K-Means?**
It groups pixels into k = 5 color clusters on a clothing photo shrunk to at most 300 pixels. The cluster centers are the dominant colors, and the biggest cluster is the most dominant one.

**Q15. How is an outfit scored?**
40% skin match (distance between the top color and the colors recommended for that skin tone), 30% color harmony (distance between top and bottom: "Too Matchy" 40, "Elegant Look" 85, "Great Contrast" 90), and 30% occasion fit (exact 100, season relaxed 70, color only 40). The weights are our design choice, not learned from data.

**Q16. Why rules and not a deep neural network?**
We had no labeled skin tone dataset or GPU. Rules run instantly and every decision can be explained. The trade-off is lower robustness.

**Q17. How does the chatbot work, and what if it fails?**
It calls the Groq API (model `openai/gpt-oss-20b`) with a system prompt that holds skin tone, occasion, body shape and style personality, and a rule to stay on fashion. If the service or internet fails, the call times out after 15 seconds and the page shows an offline reply built from our own color rules.

**Q18. Explain your architecture.**
Three layers: 13 Streamlit pages, small Python modules in `src/`, and JSON/CSV data files. The only outside service is Groq. Every function returns a dictionary with an `error` field, so bad input never crashes the app.

**Q19. How did you test it?**
12 pytest tests (skin tone classes, error dictionary, scoring formula, color math, harmony labels, offline replies), a manual full-flow test, a UI audit of 13 screens, a custom code audit tool, and a test of the live app in two browsers and on a phone.

**Q20. How is it deployed, and how is the API key protected?**
On Streamlit Community Cloud from the `main` branch of our GitHub repo. The key is stored in Cloud secrets and a gitignored `.env` file, never in the repository. The server uses `opencv-python-headless`, because it has no display.

**Q21. How accurate is it?**
We have not benchmarked it on a labeled photo set, so I can't give an accuracy percentage. It uses fixed thresholds and three categories, so lighting, makeup and filters can change the result. Measuring accuracy is our first future task.

**Q22. What are the limitations, and what about privacy and bias?**
Simple skin tone rules, Haar detection works best on front-facing faces, 150 synthetic outfits (not real products), self-selected body shape, a flat-color try-on, and shared local-file storage on the hosted server. Photos are saved to a fixed temp file, so two visitors at the same moment could overwrite each other's photo, and a fix is unique file names. The thresholds were not calibrated on a diverse dataset, so bias is possible, and we would add a fairness check.