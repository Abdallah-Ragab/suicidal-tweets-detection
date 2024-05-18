from ntscraper import Nitter

class Scraper:
    tweet_limit = 5
    def __init__(self):
        self.scraper = Nitter(instances=['https://nitter.esmailelbob.xyz'])

    def user(self, username):
        return self.scraper.get_profile_info(username)

    def tweets(self, username):
        try:
            return self.scraper.get_tweets(username, mode='user', number=self.tweet_limit)
        except Exception as e:
            return str(e)


# cli()
