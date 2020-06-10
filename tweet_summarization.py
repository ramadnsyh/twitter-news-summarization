import os
from bs4 import BeautifulSoup
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from gensim.summarization import summarize, keywords
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

def news_scrapper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get headline
    title = soup.find('h1').get_text()
    
    # Get body news
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    article = ' '.join(sentence_list)

    return title, article

def retweet_tweet(id_str):
    auth = authentication()
    retweet = requests.post(
        "https://api.twitter.com/1.1/statuses/retweet/{}.json".format(id_str),
        auth=auth
    )

    return retweet.json()

def reply_tweet(user_mention, body, tweet_id):
    auth = authentication()
    return requests.post("https://api.twitter.com/1.1/statuses/update.json", auth=auth, data={
        "status": "@{} {}".format(user_mention, body),
        "in_reply_to_status_id": tweet_id,
    }).json()


def main():
    try:
        parser = argparse.ArgumentParser(
            description='Twitter news summarization',
            prog='PROG', conflict_handler='resolve'
        )
        parser.add_argument('username', metavar='U', type=str,
                            help='Tweet username that you want to post')
        parser.add_argument('--count', type=int, default=1, nargs='?',
                    help='total tweets you want to repost')
                    
        args = parser.parse_args()
        check_authentication()
        tweets = get_user_timeline(args.username, total_tweet=args.count)
        for tweet in tweets:
            try:
                _, article = news_scrapper(tweet["entities"]["urls"][0]["url"])
                retweet = retweet_tweet(id_str=tweet["id_str"])
                id_str = retweet["id_str"]
                user_mention = retweet["entities"]["user_mentions"][0]["screen_name"]
                summarization = summarize(article, split=True)
                for summary in summarization:
                    reply = reply_tweet(user_mention=user_mention, body=summary, tweet_id=id_str)
                    id_str = reply["id_str"]
                    user_mention = reply["entities"]["user_mentions"][0]["screen_name"]
                break
            except:
                pass

    except BaseException as e:
        print(e)
        pass

if __name__ == "__main__":
    main()
    