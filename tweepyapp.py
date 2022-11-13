import tweepy

yaml.warnings({'YAMLLoadWarning': False})
conf = yaml.safe_load(open('info.yml'))

CONSUMER_KEY = conf['user']['CONSUMER_KEY']
CONSUMER_SECRET = conf['user']['CONSUMER_SECRET']
ACCESS_TOKEN = conf['user']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = conf['user']['ACCESS_TOKEN_SECRET']

def tweet(status):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(status)

status = "Automated: Still testing code!"

tweet(status)

