"""Main entry point for the Spambot Chatbot."""
import os
import asyncio
import signal
import logging
from typing import Optional
from dotenv import load_dotenv
from .telegram_bot import SpambotChatbot
from .logger import setup_logging


def validate_environment() -> Optional[str]:
    """Validate all required environment variables.
    
    Returns:
        Error message if validation fails, None otherwise
    """
    required_vars = {
        "TELEGRAM_BOT_TOKEN": "Telegram Bot Token von @BotFather",
        "ADMIN_USER_ID": "Deine Telegram User ID"
    }
    
    # Check for at least one LLM API key
    llm_keys = ["OPENAI_API_KEY", "LITELLM_API_KEY", "ANTHROPIC_API_KEY"]
    has_llm_key = any(os.getenv(key) for key in llm_keys)
    
    if not has_llm_key:
        required_vars["LLM_API_KEY"] = "Mindestens ein LLM API Key (OPENAI_API_KEY, LITELLM_API_KEY, oder ANTHROPIC_API_KEY)"
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"  - {var}: {description}")
    
    if missing:
        return (
            "❌ Fehlende Environment-Variablen:\n" + 
            "\n".join(missing) +
            "\n\nBitte erstelle eine .env Datei mit allen erforderlichen Variablen."
        )
    
    return None


def main():
    """Initialize and start the bot."""
    # Setup logging first
    log_level = os.getenv("LOG_LEVEL", "INFO")
    setup_logging(log_level=log_level)
    
    logger = logging.getLogger(__name__)
    
    # Load environment variables
    load_dotenv()
    logger.info("Environment variables loaded")
    
    # Validate environment
    error_msg = validate_environment()
    if error_msg:
        logger.error(error_msg)
        print(error_msg)
        return
    
    # Get required environment variables
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    admin_user_id = int(os.getenv("ADMIN_USER_ID"))
    
    logger.info(f"Configuration validated successfully")
    logger.info(f"Admin User ID: {admin_user_id}")
    
    # Create and run bot
    print("="*60)
    print("🤖 SPAMBOT-CHATBOT v2.0")
    print("="*60)
    
    async def run_bot():
        """Run the bot with proper signal handling."""
        bot = SpambotChatbot(
            token=telegram_token,
            admin_user_id=admin_user_id
        )
        
        logger.info("Bot initialized successfully")
        
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        
        def signal_handler(sig, frame):
            logger.info(f"Received signal {sig}, initiating shutdown...")
            for task in asyncio.all_tasks(loop):
                task.cancel()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        await bot.run()
    
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n👋 Bot gestoppt")
    except asyncio.CancelledError:
        logger.info("Bot tasks cancelled")
        print("\n👋 Bot gestoppt")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"\n❌ Fataler Fehler: {e}")
        raise


if __name__ == "__main__":
    main()