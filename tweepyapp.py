import tweepy
import yaml
import openai

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def authenticate_twitter(conf):
    auth = tweepy.OAuthHandler(conf['twitterConsumerKey'], conf['twitterConsumerSecret'])
    auth.set_access_token(conf['twitterAccessToken'], conf['twitterAccessTokenSecret'])
    return tweepy.API(auth)

def tweet(api, status):
    api.update_status(status)

def chatGPT(api_key, prompt):
    openai.api_key = api_key
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

def main():
    config = load_config('info.yml')
    api = authenticate_twitter(config['user'])
    chatGPT_api_key = config['user']['chatGPTapiKey']

    prompt = 'Write a tweet: ' + str(input("Enter prompt: "))
    print(prompt)
    status = chatGPT(chatGPT_api_key, prompt)
    print(status)

    post = input('Post to Twitter? y/n:')

    if post.lower() == 'y':
        tweet(api, status)
    else:
        print('Not posted')

if __name__ == '__main__':
    main()
