# src/test_groq.py
# Purpose: Verify our Groq API connection works and returns real AI fashion advice.

import os
from dotenv import load_dotenv
from groq import Groq

# Step 1: Load the .env file into memory so we can read GROQ_API_KEY from it
load_dotenv()

# Step 2: Read the API key from the environment (loaded from .env above)
api_key = os.getenv("GROQ_API_KEY")

# Step 3: Create a Groq client — this object handles talking to Groq's servers
client = Groq(api_key=api_key)

# Step 4: Send a chat message and ask for a response
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",  # the specific Llama 3 model we're using
    messages=[
        {
            "role": "user",
            "content": "What color suits warm skin tone?"
        }
    ]
)

# Step 5: Extract and print just the AI's text reply
ai_reply = response.choices[0].message.content
print("AI Stylist says:\n")
print(ai_reply)
