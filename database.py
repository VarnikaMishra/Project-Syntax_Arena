import sqlite3

def init_db():
    conn = sqlite3.connect('arena.db')
    cursor = conn.cursor()
    # Table for Challenges
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            difficulty TEXT,
            test_cases TEXT,
            created_at DATE DEFAULT (date('now'))
        )
    ''')
    # Table for Leaderboard/Submissions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            username TEXT PRIMARY KEY,
            xp INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()