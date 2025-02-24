import telebot
import flask
import os
from google import genai

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = flask.Flask(__name__)
# bot.set_webhook('https://1bb4-91-226-34-242.ngrok-free.app')

# Flask routes
@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    return 'Hello, World!'


# Telebot part of app
@bot.message_handler(commands=['g'])
def gemini(message):
    text = str(message.text).replace("/g ", "").strip()
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=text
        )
    result = response.text
    bot.reply_to(message, result)


if __name__ == '__main__':
    app.run(debug=True)
