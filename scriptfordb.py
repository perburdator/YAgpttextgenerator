import sqlite3

connection = sqlite3.connect('user_of_bot.db')
cur = connection.cursor()
query = f'''
CREATE TABLE IF NOT EXISTS user_of_bot(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    role TEXT,
    content TEXT,
    date DATETIME,
    tokens INTEGER,
    session_id INTEGER
);
'''
cur.execute(query)
connection.close()
