# Database utility for resume evaluation results
import sqlite3

def init_db(db_path='results.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_name TEXT,
        jd_name TEXT,
        score INTEGER,
        verdict TEXT,
        feedback TEXT,
        missing_elements TEXT
    )''')
    conn.commit()
    conn.close()

def save_result(resume_name, jd_name, score, verdict, feedback, missing_elements, db_path='results.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO results (resume_name, jd_name, score, verdict, feedback, missing_elements)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (resume_name, jd_name, score, verdict, feedback, missing_elements))
    conn.commit()
    conn.close()

def search_results(jd_filter=None, verdict_filter=None, db_path='results.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = 'SELECT * FROM results WHERE 1=1'
    params = []
    if jd_filter:
        query += ' AND jd_name LIKE ?'
        params.append(f'%{jd_filter}%')
    if verdict_filter:
        query += ' AND verdict = ?'
        params.append(verdict_filter)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows
