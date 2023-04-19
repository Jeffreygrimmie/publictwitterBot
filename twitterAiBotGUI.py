import tweepy
import yaml
import openai
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from textblob import TextBlob
import sys

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

def correct_spelling(text):
    return str(TextBlob(text).correct())

class TweetGenerator(QWidget):
    def __init__(self, api, chatGPT_api_key):
        super().__init__()
        self.api = api
        self.chatGPT_api_key = chatGPT_api_key

        layout = QVBoxLayout()

        self.prompt_label = QLabel("Enter your prompt:")
        layout.addWidget(self.prompt_label)

        self.prompt_entry = QLineEdit()
        layout.addWidget(self.prompt_entry)

        self.generate_button = QPushButton("Generate Tweet")
        self.generate_button.clicked.connect(self.generate_tweet)
        layout.addWidget(self.generate_button)

        self.generated_tweet_label = QLabel("Generated Tweet:")
        layout.addWidget(self.generated_tweet_label)

        self.generated_tweet_text = QTextEdit()
        self.generated_tweet_text.setReadOnly(True)
        layout.addWidget(self.generated_tweet_text)

        self.post_button = QPushButton("Post Tweet")
        self.post_button.clicked.connect(self.post_tweet)
        layout.addWidget(self.post_button)

        self.setLayout(layout)

    def generate_tweet(self):
        user_input = self.prompt_entry.text()
        corrected_input = correct_spelling(user_input)
        prompt = 'Write a tweet: ' + corrected_input
        status = chatGPT(self.chatGPT_api_key, prompt)
        self.generated_tweet_text.setPlainText(status)

    def post_tweet(self):
        response = QMessageBox.question(self, "Confirmation", "Are you sure you want to post the tweet?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            tweet(self.api, self.generated_tweet_text.toPlainText())
            QMessageBox.information(self, "Success", "The tweet has been posted!")
        else:
            QMessageBox.information(self, "Info", "The tweet was not posted.")

config = load_config('info.yml')
api = authenticate_twitter(config['user'])
chatGPT_api_key = config['user']['chatGPTapiKey']

app = QApplication(sys.argv)
tweet_generator = TweetGenerator(api, chatGPT_api_key)
tweet_generator.show()
sys.exit(app.exec_())
