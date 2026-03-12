#!/usr/bin/env python3
"""Quick setup validation script."""
import os
import sys
from pathlib import Path

def check_file_exists(path: str, required: bool = True) -> bool:
    """Check if a file exists."""
    exists = Path(path).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {path} {req_text}")
    return exists

def check_env_var(var: str, required: bool = True) -> bool:
    """Check if environment variable is set."""
    value = os.getenv(var)
    exists = bool(value)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {var} {req_text}")
    return exists

def main():
    print("="*60)
    print("🔍 Spambot-Chatbot Setup Validation")
    print("="*60)
    
    # Load .env if exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    errors = []
    warnings = []
    
    # Check files
    print("\n📁 Files:")
    if not check_file_exists(".env", required=True):
        errors.append(".env file missing")
    if not check_file_exists("config/personality.json", required=True):
        errors.append("personality.json missing")
    if not check_file_exists("config/timing.json", required=False):
        warnings.append("timing.json will be auto-created")
    check_file_exists("src/storage.py", required=True)
    check_file_exists("src/logger.py", required=True)
    check_file_exists("src/timing_manager.py", required=True)
    
    # Check directories
    print("\n📂 Directories:")
    check_file_exists("data/", required=True)
    check_file_exists("logs/", required=True)
    check_file_exists("config/", required=True)
    
    # Check environment variables
    print("\n🔐 Environment Variables:")
    if not check_env_var("TELEGRAM_BOT_TOKEN", required=True):
        errors.append("TELEGRAM_BOT_TOKEN not set")
    if not check_env_var("ADMIN_USER_ID", required=True):
        errors.append("ADMIN_USER_ID not set")
    
    # Check for at least one LLM API key
    has_openai = check_env_var("OPENAI_API_KEY", required=False)
    has_litellm = check_env_var("LITELLM_API_KEY", required=False)
    has_anthropic = check_env_var("ANTHROPIC_API_KEY", required=False)
    
    if not (has_openai or has_litellm or has_anthropic):
        print("❌ At least one LLM API key required (required)")
        errors.append("No LLM API key set (OPENAI_API_KEY, LITELLM_API_KEY, or ANTHROPIC_API_KEY)")
    
    check_env_var("LITELLM_API_BASE", required=False)
    check_env_var("LOG_LEVEL", required=False)
    check_env_var("LITELLM_MODEL", required=False)
    
    # Check Python packages
    print("\n📦 Python Packages:")
    packages = [
        "telegram",
        "litellm",
        "dotenv",
        "aiofiles"
    ]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            errors.append(f"Package {package} not installed")
    
    # Summary
    print("\n" + "="*60)
    if errors:
        print("❌ ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        print("\n⚠️  Please fix errors before running the bot!")
        sys.exit(1)
    elif warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
        print("\n✅ Setup is valid, but check warnings.")
    else:
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 You can start the bot with: python run.py")
    
    print("="*60)

if __name__ == "__main__":
    main()