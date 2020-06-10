import unittest
from utils import news_scrapper
from tweet_api import get_user_timeline, retweet_tweet, unretweet_tweet

class ScrapperTests(unittest.TestCase):

    def test_success_scrapping(self):
      example_url = "https://www.cnbc.com/2020/06/09/amazon-apple-facebook-microsoft-close-all-time-high-big-tech-rally.html"
      headline, article = news_scrapper(example_url)
      self.assertIsNotNone(headline)
      self.assertIsNotNone(article)

    def test_failed_scrapping(self):
      example_url = "https://twitter.com/IBKR/status/1260991718754828301"
      output = news_scrapper(example_url)
      self.assertIsNone(output)

class TweetAPITests(unittest.TestCase):

  def test_success_get_timeline(self):
    tweets = get_user_timeline("cnbctech", total_tweet=3)
    for tweet in tweets:
      self.assertIsNotNone(tweet['id_str'])
      self.assertIsNotNone(tweet['text'])
      self.assertIsNotNone(tweet["entities"]["urls"][0]["url"])
    self.assertEqual(len(tweets), 3)

  def test_failed_get_timeline(self):
    tweets = get_user_timeline("ramramdi", total_tweet=3)
    for error in tweets["errors"]:
      self.assertEqual(error["code"], 34)
      self.assertEqual(error["message"], "Sorry, that page does not exist.")

  def test_success_retweet(self):
    cnbc_tweet = get_user_timeline("cnbctech", total_tweet=1)[0]
    id_str = cnbc_tweet["id_str"]
    _ = retweet_tweet(id_str)
    tweet_before = get_user_timeline("mrmdnsyh", total_tweet=1)[0]["text"]
    self.assertEqual(cnbc_tweet["text"], tweet_before[14:])
    _ = unretweet_tweet(id_str)
    tweet_after = get_user_timeline("mrmdnsyh", total_tweet=1)[0]["text"]
    self.assertNotEqual(tweet_before, tweet_after)


if __name__ == '__main__':
    unittest.main()