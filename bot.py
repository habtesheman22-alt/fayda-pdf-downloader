#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Messages in English and Amharic
MESSAGES = {
    'en': {
        'welcome': '🇪🇹 Welcome to Fayda PDF Downloader Bot!\n\nThis bot helps you download Ethiopian National ID (Fayda) documents.',
        'help': 'Available commands:\n\n/start - Start the bot\n/documents - View available documents\n/amharic - Switch to Amharic\n/english - Switch to English\n/help - Show this message',
        'documents': 'Available Documents:',
        'form': '📋 Application Form',
        'instructions': '📖 Instructions Guide',
        'requirements': '✅ Requirements Checklist',
        'fees': '💰 Fee Information',
        'downloading': '⏳ Downloading your document...',
        'error': '❌ Error: Could not download document. Please try again.',
        'success': '✅ Document downloaded successfully!'
    },
    'am': {
        'welcome': '🇪🇹 ወደ Fayda PDF ዳውንሎደር ቦት እንኳን ደህና መጡ!\n\nይህ ቦት ያለ ኢትዮጵያ ብሔራዊ መታወቂያ (ፋይዳ) ሰነዶች ዳውንሎድ ለማድረግ ይረዳሃል።',
        'help': 'ያሉ ትዕዛዞች:\n\n/start - ቦቱን ጀምር\n/documents - ሪክስ ሰነዶች ተመልከት\n/amharic - ወደ አማርኛ ቀይር\n/english - ወደ English ቀይር\n/help - ይህን ላይ ይመልከቱ',
        'documents': 'ሪክስ ሰነዶች:',
        'form': '📋 ማመልከቻ ፍォርም',
        'instructions': '📖 መመሪያ መርሃ',
        'requirements': '✅ ሚያስፈልግ ሰነዶች ፍ�የ',
        'fees': '💰 ክፍያ መረጃ',
        'downloading': '⏳ ሰነድ ወርድ በመግባት ነው...',
        'error': '❌ ስህተት: ሰነድ ወርድ ማድረግ አልተቻለም። እባክዎ ዳግም ሞክሩ።',
        'success': '✅ ሰነድ በስኬት ወርድ ተደርጎ!'
    }
}

# PDF URLs (Update these with actual URLs)
PDF_URLS = {
    'form': 'https://example.com/fayda-form.pdf',
    'instructions': 'https://example.com/instructions.pdf',
    'requirements': 'https://example.com/requirements.pdf',
    'fees': 'https://example.com/fee-info.pdf'
}

# Store user language preference
user_language = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user_id = update.effective_user.id
    if user_id not in user_language:
        user_language[user_id] = 'en'
    
    keyboard = [
        [InlineKeyboardButton('📖 English', callback_data='lang_en'),
         InlineKeyboardButton('አማርኛ Amharic', callback_data='lang_am')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        MESSAGES['en']['welcome'],
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    user_id = update.effective_user.id
    lang = user_language.get(user_id, 'en')
    
    await update.message.reply_text(MESSAGES[lang]['help'])


async def documents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available documents"""
    user_id = update.effective_user.id
    lang = user_language.get(user_id, 'en')
    
    keyboard = [
        [InlineKeyboardButton(MESSAGES[lang]['form'], callback_data='download_form')],
        [InlineKeyboardButton(MESSAGES[lang]['instructions'], callback_data='download_instructions')],
        [InlineKeyboardButton(MESSAGES[lang]['requirements'], callback_data='download_requirements')],
        [InlineKeyboardButton(MESSAGES[lang]['fees'], callback_data='download_fees')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        MESSAGES[lang]['documents'],
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == 'lang_en':
        user_language[user_id] = 'en'
        await query.edit_message_text(text=MESSAGES['en']['welcome'])
    elif query.data == 'lang_am':
        user_language[user_id] = 'am'
        await query.edit_message_text(text=MESSAGES['am']['welcome'])
    elif query.data.startswith('download_'):
        lang = user_language.get(user_id, 'en')
        await query.edit_message_text(text=MESSAGES[lang]['downloading'])
        
        doc_type = query.data.replace('download_', '')
        try:
            pdf_url = PDF_URLS.get(doc_type)
            if pdf_url and pdf_url != 'https://example.com/fayda-form.pdf':
                await context.bot.send_document(
                    chat_id=user_id,
                    document=pdf_url
                )
                await query.edit_message_text(text=MESSAGES[lang]['success'])
            else:
                await query.edit_message_text(
                    text=MESSAGES[lang]['error'] + '\n\n📝 Note: Please update PDF URLs in .env file'
                )
        except Exception as e:
            logger.error(f"Download error: {e}")
            await query.edit_message_text(text=MESSAGES[lang]['error'])


def main() -> None:
    """Start the bot"""
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("documents", documents))
    application.add_handler(CommandHandler("amharic", lambda u, c: button_callback(u, c)))
    application.add_handler(CommandHandler("english", lambda u, c: button_callback(u, c)))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    print('🤖 Fayda PDF Downloader Bot is running...')
    print('Press Ctrl+C to stop')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
