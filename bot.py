import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from constants import *
from create_messages import *
from amazon_api import AmazonAPI
import threading
import http.server
import socketserver

bot = Bot(token=TELEGRAM_TOKEN)

#message to the user when he starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Benvenuto {update.effective_user.first_name}, mandami il link amazon di un prodotto per '
                                    'creare il post sul tuo canale!')

#TODO: identify the user who sends messages to the bot to prevent anyone with the bot's username from sending messages in the channel through it

#handle the message sent by the user (only amazon links are allowed)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    if 'amazon.it' in message_text:
        amazon_api = AmazonAPI()

        #retry product information from amazon api
        product = amazon_api.get_product_from_url(message_text)

        #create the post for the channel
        formatted_message = create_product_post(product)

        #send the post to the channel
        await bot.send_message(chat_id=CHANNEL_ID, text=formatted_message, parse_mode='HTML')

app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

import os
  # adjust as per your code

# Start a dummy HTTP server to satisfy Koyeb's health check
def fake_web_server():
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=fake_web_server).start()

# Set up your bot
app = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

# Your command handlers, etc...
# app.add_handler(...)

# Run the bot in polling mode

app.run_polling()
