# -*- coding: utf-8 -*-
""" This script removes old tweets and stores them in sqlite
"""

import tweepy
from datetime import datetime
import sqlite3

# Twitter Constants: add your own
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
USER_NAME = ''

# Local Constants: add your own
sqlite_file_path = ''

# Connect To Your Twitter Account via Tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

# Checking Twitter credentials
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# For the account name
def delete_and_move_tweets(sqlite_path, account_name, days=365):
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()

    # For each tweet
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='@' + account_name).items():
        # Get the tweet id
        tweet_id = tweet._json['id']
        print(f"Handling tweet: {tweet_id}")

        # Get the datetime of the tweet
        status_date = datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

        # if it's an old tweet
        if (datetime.utcnow() - status_date).days > days:
            # save it to sqlite
            try:
                cur.execute('''INSERT INTO tweets (tweetId, tweet_timestamp, tweet_text)
                VALUES (?, ?, ?)''', (tweet._json['id'], tweet._json['created_at'], tweet._json['text']))
            except sqlite3.IntegrityError:
                continue

            # & Delete the tweet
            api.destroy_status(tweet_id)
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Deleting', tweet_id)

    conn.commit()
    cur.close()


if __name__ == '__main__':
    delete_and_move_tweets(account_name=USER_NAME, days=1000, sqlite_path=sqlite_file_path)
