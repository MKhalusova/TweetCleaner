import sqlite3

# add your sqlite file path
db_path = ""

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''CREATE TABLE tweets (tweetId TEXT PRIMARY KEY, tweet_timestamp TIMESTAMP, 
tweet_text TEXT)''')

conn.commit()
cur.close()



