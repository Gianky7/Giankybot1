import os
import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Path DB configurabile via env (per hosting con volume)
DB_PATH = os.getenv('DB_PATH', 'giankybot.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        wallet TEXT,
        balance INTEGER DEFAULT 100,
        spins INTEGER DEFAULT 3
    )
    ''')
    conn.commit()
    conn.close()

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Benvenuto nel bot GiankyCoin 🎰")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("ℹ️ Info sul bot...")

async def buy_spins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Compra spin...")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Restart registrazione...")

# === Avvio applicazione (polling) ===
def build_app():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(info, pattern="^info$"))
    app.add_handler(CallbackQueryHandler(buy_spins, pattern="^buy_spins$"))
    app.add_handler(CallbackQueryHandler(restart, pattern="^restart$"))
    return app

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN non impostato")
    app = build_app()
    app.run_polling(drop_pending_updates=True)
