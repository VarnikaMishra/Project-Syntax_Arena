from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import json
import subprocess
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSubmission(BaseModel):
    username: str
    challenge_id: int
    language: str
    code: str

def clean_output(text: str) -> str:
    return text.strip().lower()

@app.get("/questions")
async def get_questions():
    conn = sqlite3.connect('arena.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, difficulty FROM challenges")
    questions = [
        {"id": r[0], "title": r[1], "description": r[2], "difficulty": r[3]} 
        for r in cursor.fetchall()
    ]
    conn.close()
    return questions

@app.post("/judge")
async def judge(sub: CodeSubmission):
    conn = sqlite3.connect('arena.db')
    cursor = conn.cursor()
    cursor.execute("SELECT test_cases, difficulty FROM challenges WHERE id = ?", (sub.challenge_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    test_cases = json.loads(row[0])
    difficulty = row[1]
    passed_count = 0
    
    for tc in test_cases:
        temp_file = "temp_solution.py"
        try:
            with open(temp_file, "w") as f:
                f.write(sub.code)

            # NOTE: If 'python' fails, change it to 'python3' below
            process = subprocess.Popen(
                ['python', temp_file], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )

            try:
                stdout, stderr = process.communicate(input=tc["input"], timeout=2)
                actual = clean_output(stdout)
                expected = clean_output(str(tc["output"]))

                if actual == expected:
                    passed_count += 1
            except subprocess.TimeoutExpired:
                process.kill()
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    is_passed = (passed_count == len(test_cases))
    
    if is_passed:
        xp_map = {"Easy": 10, "Medium": 20, "Hard": 30}
        reward = xp_map.get(difficulty, 50)
        
        # Update Leaderboard
        cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard (username TEXT PRIMARY KEY, xp INTEGER)")
        cursor.execute("INSERT OR IGNORE INTO leaderboard (username, xp) VALUES (?, 0)", (sub.username,))
        cursor.execute("UPDATE leaderboard SET xp = xp + ? WHERE username = ?", (reward, sub.username))
        conn.commit()
        msg = f"Passed! +{reward} XP"
    else:
        msg = f"Failed. Passed {passed_count}/{len(test_cases)}"

    conn.close()
    return {"passed": is_passed, "message": msg}