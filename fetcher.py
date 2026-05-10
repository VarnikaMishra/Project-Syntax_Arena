import os
import json
import sqlite3
from google import genai
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Initialize the new Client
# The client automatically handles auth if GEMINI_API_KEY is in your environment
client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_daily_questions():
    prompt = """
    Generate 15 coding challenges: 5 Easy, 5 Medium, 5 Hard.
    Return ONLY a raw JSON array. No markdown, no backticks.
    Format: [{"title": "Name", "desc": "Prompt", "difficulty": "Easy", "test_cases": [{"input": "1", "output": "2"}]}]
    """
    
    try:
        # Using the new generate_content method
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        # Clean response text (the new SDK is better at returning clean JSON)
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.splitlines()[1:-1]
            raw_text = "".join(raw_text)
            
        challenges = json.loads(raw_text)
        
        # Save to SQLite
        conn = sqlite3.connect('arena.db')
        cursor = conn.cursor()
        for c in challenges:
            cursor.execute('''
                INSERT INTO challenges (title, description, difficulty, test_cases)
                VALUES (?, ?, ?, ?)
            ''', (c['title'], c['desc'], c['difficulty'], json.dumps(c['test_cases'])))
        conn.commit()
        conn.close()
        print("✅ Success: 15 questions synced for today.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_daily_questions()