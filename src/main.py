"""Main entry point for the Spambot Chatbot."""
import os
from dotenv import load_dotenv
from .telegram_bot import SpambotChatbot


def main():
    """Initialize and start the bot."""
    # Load environment variables
    load_dotenv()
    
    # Get required environment variables
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    admin_user_id = os.getenv("ADMIN_USER_ID")
    
    # Validate environment variables
    if not telegram_token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN nicht gefunden! "
            "Bitte .env Datei erstellen und Token eintragen."
        )
    
    if not admin_user_id:
        raise ValueError(
            "ADMIN_USER_ID nicht gefunden! "
            "Bitte .env Datei erstellen und deine Telegram User ID eintragen."
        )
    
    try:
        admin_user_id = int(admin_user_id)
    except ValueError:
        raise ValueError("ADMIN_USER_ID muss eine Zahl sein!")
    
    # Verify LLM API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "⚠️  WARNUNG: OPENAI_API_KEY nicht gesetzt! "
            "Der Bot wird nicht funktionieren."
        )
    
    # Create and run bot
    print("="*50)
    print("🤖 SPAMBOT-CHATBOT")
    print("="*50)
    
    bot = SpambotChatbot(
        token=telegram_token,
        admin_user_id=admin_user_id
    )
    
    bot.run()


if __name__ == "__main__":
    main()