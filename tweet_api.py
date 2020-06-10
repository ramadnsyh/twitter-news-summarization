import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import argparse

load_dotenv()

def env_vars(request):
    return os.environ.get(request, None)

def check_authentication():
    auth = authentication()
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    requests.get(url, auth=auth)

def authentication():
    API_KEY = env_vars("API_KEY")
    API_SECRET_KEY = env_vars("API_SECRET_KEY")
    ACCESS_TOKEN = env_vars("ACCESS_TOKEN")
    ACCESS_SECRET_TOKEN = env_vars("ACCESS_SECRET_TOKEN")
    auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    return auth

def get_user_timeline(username, total_tweet=10):
    auth = authentication()
    tweets = requests.get(
        "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={}&count={}".format(username, total_tweet),
        auth=auth
    )
    return tweets.json()

def retweet_tweet(id_str):
    auth = authentication()
    retweet = requests.post(
        "https://api.twitter.com/1.1/statuses/retweet/{}.json".format(id_str),
        auth=auth
    )

    return retweet.json()

def unretweet_tweet(id_str):
  auth = authentication()
  unretweet = requests.post(
      "https://api.twitter.com/1.1/statuses/unretweet/{}.json".format(id_str),
      auth=auth
  )

  return unretweet.json()

def reply_tweet(user_mention, body, tweet_id):
    auth = authentication()
    return requests.post("https://api.twitter.com/1.1/statuses/update.json", auth=auth, data={
        "status": "@{} {}".format(user_mention, body),
        "in_reply_to_status_id": tweet_id,
    }).json()