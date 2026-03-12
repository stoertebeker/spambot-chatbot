"""Telegram bot handler."""
import os
import random
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from typing import Set, Optional

from .llm_handler import LLMHandler
from .personality import PersonalityManager


class SpambotChatbot:
    """Telegram bot that engages with spammers."""
    
    def __init__(self, token: str, admin_user_id: int):
        self.token = token
        self.admin_user_id = admin_user_id
        self.active_targets: Set[int] = set()
        
        # Initialize personality and LLM
        self.personality = PersonalityManager()
        self.llm = LLMHandler(
            system_prompt=self.personality.get_system_prompt()
        )
        
        # Timing configuration for natural behavior
        self.min_delay = 2.0  # Minimum delay in seconds
        self.max_delay = 8.0  # Maximum delay in seconds
        self.chars_per_second = random.uniform(3.5, 6.0)  # Typing speed
        self.occasional_long_pause_chance = 0.15  # 15% chance for long pause
        self.long_pause_duration = (30, 180)  # 30 seconds to 3 minutes
        
        # Build application
        self.app = Application.builder().token(token).build()
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register command and message handlers."""
        # Command handlers (only for admin)
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("add", self.add_target_command))
        self.app.add_handler(CommandHandler("remove", self.remove_target_command))
        self.app.add_handler(CommandHandler("list", self.list_targets_command))
        self.app.add_handler(CommandHandler("reset", self.reset_conversation_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(CommandHandler("warmstart", self.warm_start_command))
        self.app.add_handler(CommandHandler("timing", self.timing_command))
        
        # Message handler for active targets
        # Message handler for forwarded messages (warm start)
        self.app.add_handler(
            MessageHandler(
                filters.FORWARDED & filters.TEXT,
                self.handle_forwarded_message
            )
        )
        
        # Message handler for active targets
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message
            )
        )
    
    def _is_admin(self, user_id: int) -> bool:
        """Check if user is admin."""
        return user_id == self.admin_user_id
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        if not self._is_admin(update.effective_user.id):
            return
        
        welcome_msg = (
            f"🤖 Spambot-Chatbot aktiv!\n\n"
            f"Persona: {self.personality.get_name()}\n\n"
            f"Verfügbare Befehle:\n"
            f"/add <chat_id> - Füge einen Spammer hinzu\n"
            f"/remove <chat_id> - Entferne einen Spammer\n"
            f"/list - Zeige aktive Targets\n"
            f"/reset <chat_id> - Setze Konversation zurück\n"
            f"/warmstart <chat_id> - Analysiere bisherige Nachrichten\n"
            f"/timing - Zeige/ändere Timing-Einstellungen\n"
            f"/status - Zeige Bot-Status\n"
            f"/help - Zeige Hilfe"
        )
        await update.message.reply_text(welcome_msg)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        if not self._is_admin(update.effective_user.id):
            return
        
        help_msg = (
            "📖 Anleitung:\n\n"
            "1. Wenn dich ein Spammer kontaktiert, kopiere die Chat-ID\n"
            "2. Füge die Chat-ID mit /add <chat_id> hinzu\n"
            "3. Der Bot wird automatisch auf Nachrichten antworten\n"
            "4. Mit /remove <chat_id> kannst du den Bot stoppen\n\n"
            "Hinweis: Die Chat-ID siehst du, wenn du eine Nachricht \n"
            "vom Spammer weiterleitest (@userinfobot kann helfen)."
        )
        await update.message.reply_text(help_msg)
    
    async def add_target_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Add a spammer chat to active targets."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Bitte gib eine Chat-ID an:\n/add <chat_id>"
            )
            return
        
        try:
            chat_id = int(context.args[0])
            self.active_targets.add(chat_id)
            await update.message.reply_text(
                f"✅ Chat {chat_id} zur Zielliste hinzugefügt!\n"
                f"Der Bot wird nun auf Nachrichten antworten."
            )
        except ValueError:
            await update.message.reply_text("❌ Ungültige Chat-ID!")
    
    async def remove_target_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Remove a spammer from active targets."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Bitte gib eine Chat-ID an:\n/remove <chat_id>"
            )
            return
        
        try:
            chat_id = int(context.args[0])
            if chat_id in self.active_targets:
                self.active_targets.remove(chat_id)
                await update.message.reply_text(
                    f"✅ Chat {chat_id} von der Zielliste entfernt!"
                )
            else:
                await update.message.reply_text(
                    f"❌ Chat {chat_id} war nicht in der Zielliste."
                )
        except ValueError:
            await update.message.reply_text("❌ Ungültige Chat-ID!")
    
    async def list_targets_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List all active targets."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not self.active_targets:
            await update.message.reply_text("📭 Keine aktiven Targets.")
            return
        
        target_list = "\n".join(
            f"• {chat_id} ({self.llm.get_conversation_length(chat_id)} Nachrichten)"
            for chat_id in self.active_targets
        )
        await update.message.reply_text(
            f"📋 Aktive Targets ({len(self.active_targets)}):\n\n{target_list}"
        )
    
    async def reset_conversation_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Reset conversation for a specific chat."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Bitte gib eine Chat-ID an:\n/reset <chat_id>"
            )
            return
        
        try:
            chat_id = int(context.args[0])
            self.llm.reset_conversation(chat_id)
            await update.message.reply_text(
                f"✅ Konversation für Chat {chat_id} zurückgesetzt!"
            )
        except ValueError:
            await update.message.reply_text("❌ Ungültige Chat-ID!")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show bot status."""
        if not self._is_admin(update.effective_user.id):
            return
        
        status_msg = (
            f"🤖 Bot Status\n\n"
            f"Persona: {self.personality.get_name()}\n"
            f"Model: {self.llm.model}\n"
            f"Aktive Targets: {len(self.active_targets)}\n"
            f"Admin ID: {self.admin_user_id}"
        )
        await update.message.reply_text(status_msg)
    
    async def warm_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Analyze previous conversation to adopt user's style."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Bitte gib eine Chat-ID an:\n/warmstart <chat_id>\n\n"
                "📝 So funktioniert's:\n"
                "1. Verwende /warmstart <chat_id>\n"
                "2. Leite mir DEINE Nachrichten aus dem Chat weiter\n"
                "3. Ich analysiere deinen Schreibstil\n"
                "4. Dann verwende /add <chat_id> um zu starten"
            )
            return
        
        try:
            chat_id = int(context.args[0])
            
            # Store chat_id in context for forwarded messages
            if 'warm_start_chat' not in context.user_data:
                context.user_data['warm_start_chat'] = chat_id
            
            existing_examples = self.llm.get_style_examples(chat_id)
            
            await update.message.reply_text(
                f"✅ Warm Start Modus für Chat {chat_id} aktiviert!\n\n"
                f"📨 Leite mir jetzt 5-10 DEINER Nachrichten aus dem Gespräch weiter.\n\n"
                f"Bereits gespeichert: {len(existing_examples)} Beispiele\n\n"
                f"Wenn fertig, sende /warmstart {chat_id} erneut für eine Analyse."
            )
        except ValueError:
            await update.message.reply_text("❌ Ungültige Chat-ID!")
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle forwarded messages for warm start style learning."""
        if not self._is_admin(update.effective_user.id):
            return
        
        # Check if we're in warm start mode
        if 'warm_start_chat' not in context.user_data:
            return
        
        chat_id = context.user_data['warm_start_chat']
        message_text = update.message.text
        
        if message_text:
            # Add this message as a style example
            self.llm.add_style_examples(chat_id, [message_text])
            
            # Get current count
            examples = self.llm.get_style_examples(chat_id)
            
            await update.message.reply_text(
                f"✅ Nachricht hinzugefügt! ({len(examples)} gespeichert)\n\n"
                f"Leite weitere Nachrichten weiter oder sende:\n"
                f"/warmstart {chat_id} für Analyse"
            )
    
    async def timing_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show or modify timing settings."""
        if not self._is_admin(update.effective_user.id):
            return
        
        # If we have a warm_start_chat, show style analysis
        if 'warm_start_chat' in context.user_data:
            chat_id = context.user_data['warm_start_chat']
            examples = self.llm.get_style_examples(chat_id)
            
            if examples:
                await update.message.reply_text(
                    f"🔍 Analysiere Schreibstil für Chat {chat_id}...\n\n"
                    f"Basis: {len(examples)} Nachrichten"
                )
                
                # Analyze style
                analysis = await self.llm.analyze_user_style(examples)
                
                await update.message.reply_text(
                    f"📊 Stil-Analyse:\n\n{analysis}\n\n"
                    f"Der Bot wird versuchen, diesen Stil zu imitieren!"
                )
                
                # Clear warm start mode
                del context.user_data['warm_start_chat']
                return
        
        timing_info = (
            f"⏱️ Timing-Einstellungen:\n\n"
            f"Min. Verzögerung: {self.min_delay}s\n"
            f"Max. Verzögerung: {self.max_delay}s\n"
            f"Tippgeschwindigkeit: {self.chars_per_second:.1f} Zeichen/s\n"
            f"Pause-Wahrscheinlichkeit: {self.occasional_long_pause_chance*100:.0f}%\n"
            f"Pausendauer: {self.long_pause_duration[0]}-{self.long_pause_duration[1]}s"
        )
        await update.message.reply_text(timing_info)
    
    def _calculate_typing_delay(self, text: str) -> float:
        """Calculate realistic typing delay based on message length."""
        # Base delay on text length
        base_delay = len(text) / self.chars_per_second
        
        # Add some randomness
        variation = random.uniform(0.8, 1.3)
        delay = base_delay * variation
        
        # Ensure within min/max bounds
        delay = max(self.min_delay, min(self.max_delay, delay))
        
        # Occasionally add a longer pause (person is busy)
        if random.random() < self.occasional_long_pause_chance:
            extra_pause = random.uniform(*self.long_pause_duration)
            delay += extra_pause
            print(f"[Timing] Längere Pause: {extra_pause:.1f}s (wirkt beschäftigt)")
        
        return delay
    
    async def _send_typing_action(self, chat_id: int, duration: float) -> None:
        """Send typing indicator for a realistic duration."""
        # Telegram typing indicator lasts ~5 seconds, so we need to repeat it
        iterations = int(duration / 5) + 1
        
        for i in range(iterations):
            try:
                await self.app.bot.send_chat_action(
                    chat_id=chat_id,
                    action="typing"
                )
                
                # Wait 5 seconds or remaining time
                wait_time = min(5, duration - (i * 5))
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
            except Exception as e:
                print(f"[Typing] Fehler beim Senden des Typing-Indikators: {e}")
                break
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming messages from targets with natural timing."""
        chat_id = update.effective_chat.id
        
        # Only respond to active targets
        if chat_id not in self.active_targets:
            return
        
        user_message = update.message.text
        print(f"[Chat {chat_id}] Nachricht empfangen: {user_message[:50]}...")
        
        # Small initial delay (reading the message)
        reading_delay = random.uniform(1.0, 3.0)
        await asyncio.sleep(reading_delay)
        
        # Get LLM response
        response = await self.llm.get_response(chat_id, user_message)
        
        # Calculate realistic typing delay
        typing_delay = self._calculate_typing_delay(response)
        print(f"[Timing] Verzögerung: {typing_delay:.1f}s für {len(response)} Zeichen")
        
        # Show typing indicator while "composing" the message
        await self._send_typing_action(chat_id, typing_delay)
        
        # Send response
        await update.message.reply_text(response)
        print(f"[Chat {chat_id}] Antwort gesendet: {response[:50]}...")
    
    def run(self) -> None:
        """Start the bot."""
        print(f"🚀 Bot startet als '{self.personality.get_name()}'...")
        print(f"Admin User ID: {self.admin_user_id}")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)