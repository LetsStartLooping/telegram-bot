from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ApplicationHandlerStop, TypeHandler
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

# Read list of approved users from .env file.
# You can maintain your own list in the way you like
APPROVED_USERS = os.getenv('APPROVED_USERS').split(",")

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Note the way I am loading Approved users, it comes as list of strings.
    # So, I am converting `update.effective_user.id` to string
    if str(update.effective_user.id) in APPROVED_USERS:
        pass
    else:
        await update.effective_message.reply_text("Hey! You are not authorized to use this Bot!")
        # Stop Further Processing
        raise ApplicationHandlerStop


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=update.message.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Hi There! How are you doing today!")
    
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=f"Your Chat Id is: {update.effective_chat.id}")


if __name__ == "__main__":

    # 1. Create Bot application using BOT TOKEN
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 2. Create a Command Handler to trigger the method `start` 
    # whenever the user issues the command `/start` 
    start_handler = CommandHandler("start", start)

    # 2a. Create a Message Handler to trigger the method `echo` 
    # whenever the user sends a regular message
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # 2b. Create a Command Handler to trigger the method `chat_id` 
    # whenever the user issues the command `/chat_id` 
    chat_id_handler = CommandHandler("chat_id", chat_id)

    # 2c. Check User Handler
    check_user_handler = TypeHandler(Update, check_user)

    # 3. Assign the start handler to the application.
    application.add_handler(start_handler)

    # 3a. Assign the message handler to the application
    application.add_handler(echo_handler)

    # 3a. Assign the command handler to the application
    application.add_handler(chat_id_handler)

    # 3c. Add Check user handler to the application with Group -1
    # Group = -1 ensures this gets called before any other handler.
    application.add_handler(check_user_handler, group=-1)

    # 4. Initialize and Start the Telegram App
    application.run_polling()