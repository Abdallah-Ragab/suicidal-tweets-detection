from ntscraper import Nitter

class Scraper:
    def __init__(self, tweet_limit=10):
        self.tweet_limit = tweet_limit
        self.scraper = Nitter(instances=['https://nitter.esmailelbob.xyz'])

    def user(self, username):
        return self.scraper.get_profile_info(username)

    def tweets(self, username):
        try:
            return self.scraper.get_tweets(username, mode='user', number=self.tweet_limit)
        except Exception as e:
            return False