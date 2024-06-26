from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from gemini import gemini_response, gemini_chat
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram access token and bot username from environment variables
TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")

# Command handlers
async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello there! Use /hello to get a greeting!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('I can help you with the following commands:\n/hello - Get a greeting\n/start - Get a welcome message\n/help - Get a list of commands')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('This is a custom command!')

# Responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type  # private, group, supergroup, channel
    text: str = update.message.text  # The message text

    print(f'User ({update.message.chat.first_name}) in {message_type}: "{text}"')

    if message_type == 'private':
        response: str = gemini_chat(text)
        await update.message.reply_text(response)
    elif message_type == 'group':
        response: str = gemini_response(text)
        await update.message.reply_text(response)

    print(f'Bot Response: "{response}"')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = ApplicationBuilder().token(TELEGRAM_ACCESS_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("hello", hello_command))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handler
    app.add_error_handler(error)

    # Start polling
    print("Bot is running...")
    app.run_polling()
