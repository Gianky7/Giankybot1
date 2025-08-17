from bot_patched import build_app

if __name__ == "__main__":
    app = build_app()
    app.run_polling(drop_pending_updates=True)
