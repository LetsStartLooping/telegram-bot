from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Loading ENV file for values like BOT TOEKN
load_dotenv('keys.env')

# This is populating BOT TOKEN from an environment file. You can have your own logic to do the same.
BOT_TOKEN = os.getenv('BOT_TOKEN') 

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=update.message.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Hi There! How are you doing today!")


if __name__ == "__main__":

    # 1. Create Bot application using BOT TOKEN
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 2. Create a Command Handler to trigger the method `start` 
    # whenever the user issues the command `/start` 
    start_handler = CommandHandler("start", start)

    # 2a. Create a Message Handler to trigger the method `echo` 
    # whenever the user sends a regular message
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # 3. Assign the start handler to the application.
    application.add_handler(start_handler)

    # 3a. Assign the message handler to the application
    application.add_handler(echo_handler)

    # 4. Initialize and Start the Telegram App
    application.run_polling()