"""Main entry point for the Telegram Userbot."""
import os
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
from .userbot import SpamResponderUserbot
from .storage import BotStorage
from .logger import setup_logging


def validate_environment() -> Optional[str]:
    """Validate all required environment variables.
    
    Returns:
        Error message if validation fails, None otherwise
    """
    required_vars = {
        "TELEGRAM_API_ID": "Telegram API ID from https://my.telegram.org",
        "TELEGRAM_API_HASH": "Telegram API Hash from https://my.telegram.org"
    }
    
    # Check for at least one LLM API key
    llm_keys = ["OPENAI_API_KEY", "LITELLM_API_KEY", "ANTHROPIC_API_KEY"]
    has_llm_key = any(os.getenv(key) for key in llm_keys)
    
    if not has_llm_key:
        required_vars["LLM_API_KEY"] = "At least one LLM API Key (OPENAI_API_KEY, LITELLM_API_KEY, or ANTHROPIC_API_KEY)"
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"  - {var}: {description}")
    
    if missing:
        return (
            "❌ Missing Environment Variables:\n" + 
            "\n".join(missing) +
            "\n\nPlease create a .env file with all required variables."
        )
    
    return None


async def main():
    """Initialize and start the userbot."""
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
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH")
    
    logger.info(f"Configuration validated successfully")
    
    # Try to load existing session
    storage = BotStorage()
    session_string = storage.load_session()
    
    if session_string:
        logger.info("Found existing session, will attempt to use it")
        print("✅ Found existing session")
    else:
        logger.info("No existing session found, will need to login")
        print("📱 First time login - you'll need to enter your phone number and code")
    
    # Create and run userbot
    print("="*60)
    print("🤖 TELEGRAM SPAM RESPONDER USERBOT v3.0")
    print("="*60)
    
    userbot = None
    try:
        userbot = SpamResponderUserbot(
            api_id=api_id,
            api_hash=api_hash,
            session_string=session_string if session_string else None
        )
        
        logger.info("Userbot initialized successfully")
        await userbot.run()
        
    except KeyboardInterrupt:
        logger.info("Userbot stopped by user")
        print("\n👋 Userbot stopped")
    except asyncio.CancelledError:
        logger.info("Userbot tasks cancelled")
        print("\n👋 Userbot stopped")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"\n❌ Fatal error: {e}")
        raise
    finally:
        if userbot:
            try:
                await userbot.stop()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")


if __name__ == "__main__":
    asyncio.run(main())