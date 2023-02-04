import tweepy
import yaml
import openai

def tweet(status):
    auth = tweepy.OAuthHandler(twitterConsumerKey, twitterConsumerSecret)
    auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)
    api = tweepy.API(auth)
    api.update_status(status)

def chatGPT(prompt):
    model_engine = "text-davinci-003"
    max_tokens = 280
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text

yaml.warnings({'YAMLLoadWarning': False})
conf = yaml.safe_load(open('info.yml'))
twitterConsumerKey = conf['user']['twitterConsumerKey']
twitterConsumerSecret = conf['user']['twitterConsumerSecret']
twitterAccessToken = conf['user']['twitterAccessToken']
twitterAccessTokenSecret = conf['user']['twitterAccessTokenSecret']
openai.api_key = conf['user']['chatGPTapiKey']

prompt = 'Write a tweet: ' + str(input("Enter prompt: "))
print(prompt)
status = chatGPT(prompt)
print(status)

post = input('Post to Twitter? y/n:')

if post == 'y':
    tweet(status)
else:
    print('Not posted')

