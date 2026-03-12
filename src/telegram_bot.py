"""Telegram bot handler."""
import os
import random
import asyncio
import logging
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
from .storage import BotStorage
from .timing_manager import TimingManager

logger = logging.getLogger(__name__)


class SpambotChatbot:
    """Telegram bot that engages with spammers."""
    
    def __init__(self, token: str, admin_user_id: int):
        self.token = token
        self.admin_user_id = admin_user_id
        
        logger.info("Initializing Spambot Chatbot...")
        
        # Initialize storage
        self.storage = BotStorage()
        
        # Load saved state
        self.active_targets, saved_style_examples = self.storage.load_state()
        logger.info(f"Loaded {len(self.active_targets)} active targets from storage")
        
        # Initialize personality and LLM
        self.personality = PersonalityManager()
        self.llm = LLMHandler(
            system_prompt=self.personality.get_system_prompt()
        )
        
        # Restore saved style examples
        if saved_style_examples:
            self.llm.user_style_examples = saved_style_examples
            logger.info(f"Restored style examples for {len(saved_style_examples)} chats")
        
        # Initialize timing manager
        self.timing = TimingManager()
        
        # Load timing configuration
        self.min_delay = self.timing.get("min_delay", 2.0)
        self.max_delay = self.timing.get("max_delay", 8.0)
        self.chars_per_second = random.uniform(
            self.timing.get("chars_per_second_min", 3.5),
            self.timing.get("chars_per_second_max", 6.0)
        )
        self.occasional_long_pause_chance = self.timing.get("long_pause_chance", 0.15)
        self.long_pause_duration = (
            self.timing.get("long_pause_min", 30),
            self.timing.get("long_pause_max", 180)
        )
        
        logger.info(f"Timing configured: {self.chars_per_second:.1f} chars/s, "
                   f"pause chance: {self.occasional_long_pause_chance*100:.0f}%")
        
        # Build application
        self.app = Application.builder().token(token).build()
        self._register_handlers()
        
        logger.info("Bot initialization complete")
    
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
        self.app.add_handler(CommandHandler("import", self.import_chat_command))
        self.app.add_handler(CommandHandler("done", self.done_import_command))
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
            f"/import - Importiere Chat-Verlauf (einfach Nachrichten weiterleiten!)\n"
            f"/add <chat_id> - Füge einen Spammer hinzu (ohne History)\n"
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
            "**Methode 1: Mit Chat-Verlauf (empfohlen)**\n"
            "1. Sende /import\n"
            "2. Leite ALLE Nachrichten aus dem Spammer-Chat weiter\n"
            "3. Sende /done wenn fertig\n"
            "→ Bot kennt die History und deinen Stil!\n\n"
            "**Methode 2: Ohne History**\n"
            "1. Finde die Chat-ID (@userinfobot hilft)\n"
            "2. Sende /add <chat_id>\n"
            "→ Bot antwortet auf neue Nachrichten\n\n"
            "**Stoppen:**\n"
            "/remove <chat_id> - Bot stoppen"
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
            
            # Save state
            self._save_state()
            
            logger.info(f"Added target: {chat_id}")
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
                
                # Save state
                self._save_state()
                
                logger.info(f"Removed target: {chat_id}")
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
        """Handle forwarded messages for import mode."""
        if not self._is_admin(update.effective_user.id):
            return
        
        message_text = update.message.text
        if not message_text:
            return
        
        # Check if we're in import mode
        if context.user_data.get('import_mode', False):
            forward_from = update.message.forward_from
            forward_from_chat = update.message.forward_from_chat
            
            # Try to determine who sent the message
            is_from_admin = False
            chat_id = None
            
            if forward_from:
                # Message forwarded from a user
                is_from_admin = (forward_from.id == self.admin_user_id)
                chat_id = forward_from.id
            elif forward_from_chat:
                # Message forwarded from a chat/channel
                chat_id = forward_from_chat.id
            
            if chat_id is None:
                await update.message.reply_text(
                    "⚠️ Konnte Chat-ID nicht ermitteln. Stelle sicher, dass die Nachricht weitergeleitet wurde."
                )
                return
            
            # Get timestamp from the original message
            # forward_date is the original send time
            timestamp = update.message.forward_date if update.message.forward_date else update.message.date
            
            # Store the message with timestamp
            import_messages = context.user_data.get('import_messages', [])
            import_messages.append({
                'text': message_text,
                'is_from_admin': is_from_admin,
                'chat_id': chat_id,
                'timestamp': timestamp
            })
            context.user_data['import_messages'] = import_messages
            
            role_icon = "👤" if is_from_admin else "💬"
            await update.message.reply_text(
                f"{role_icon} Nachricht #{len(import_messages)} gespeichert\n"
                f"Wenn fertig: /done"
            )
            return
        
        # Check if we're in warm start mode
        if 'warm_start_chat' in context.user_data:
            chat_id = context.user_data['warm_start_chat']
            
            # Add this message as a style example
            self.llm.add_style_examples(chat_id, [message_text])
            
            # Get current count
            examples = self.llm.get_style_examples(chat_id)
            
            await update.message.reply_text(
                f"✅ Nachricht hinzugefügt! ({len(examples)} gespeichert)\n\n"
                f"Leite weitere Nachrichten weiter oder sende:\n"
                f"/warmstart {chat_id} für Analyse"
            )
            return
    
    async def import_chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Import chat history - simplified version."""
        if not self._is_admin(update.effective_user.id):
            return
        
        await update.message.reply_text(
            "📥 **Chat Import - Super einfach!**\n\n"
            "📝 So geht's:\n"
            "1. Gehe zum Chat mit dem Spammer\n"
            "2. Wähle ALLE Nachrichten aus (gedrückt halten)\n"
            "3. Klicke 'Weiterleiten' und sende sie mir\n"
            "4. Ich erkenne automatisch, wer wer ist\n\n"
            "⚠️ Wichtig: Leite die Nachrichten in der richtigen Reihenfolge weiter\n"
            "(von alt nach neu)\n\n"
            "Wenn du fertig bist, sende: /done"
        )
        
        # Activate import mode
        context.user_data['import_mode'] = True
        context.user_data['import_messages'] = []
    
    async def done_import_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Finalize the chat import."""
        if not self._is_admin(update.effective_user.id):
            return
        
        if not context.user_data.get('import_mode', False):
            await update.message.reply_text(
                "❌ Kein aktiver Import.\n"
                "Starte erst mit /import"
            )
            return
        
        import_messages = context.user_data.get('import_messages', [])
        
        if not import_messages:
            await update.message.reply_text(
                "❌ Keine Nachrichten zum Importieren.\n"
                "Leite zuerst Nachrichten weiter!"
            )
            return
        
        # Determine the chat_id (should be consistent across all messages)
        chat_id = import_messages[0]['chat_id']
        
        # Sort messages by timestamp to ensure chronological order
        import_messages.sort(key=lambda m: m.get('timestamp', 0))
        
        # Separate user and other messages
        user_messages = []
        other_messages = []
        all_conversation = []
        
        for msg in import_messages:
            text = msg['text']
            
            if msg['is_from_admin']:
                user_messages.append(text)
                all_conversation.append(('user', text))
            else:
                other_messages.append(text)
                all_conversation.append(('assistant', text))
        
        # Add user messages as style examples
        if user_messages:
            self.llm.add_style_examples(chat_id, user_messages)
            logger.info(f"Added {len(user_messages)} style examples for chat {chat_id}")
        
        # Build conversation history
        conversation = self.llm._get_conversation(chat_id)
        
        # Add all messages to conversation
        for role, text in all_conversation:
            conversation.append({"role": role, "content": text})
        
        # Limit conversation history to last 20 messages (+ system)
        if len(conversation) > 21:
            self.llm.conversation_history[chat_id] = [conversation[0]] + conversation[-20:]
        
        # Add to active targets
        self.active_targets.add(chat_id)
        
        # Save state
        self._save_state()
        
        # Clear import mode
        context.user_data['import_mode'] = False
        context.user_data['import_messages'] = []
        
        await update.message.reply_text(
            f"✅ Chat-Import erfolgreich abgeschlossen!\n\n"
            f"📊 Statistik:\n"
            f"• Deine Nachrichten: {len(user_messages)}\n"
            f"• Spammer-Nachrichten: {len(other_messages)}\n"
            f"• Gesamt: {len(import_messages)}\n\n"
            f"🎯 Chat {chat_id} ist jetzt aktiv!\n"
            f"Der Bot kennt den Gesprächsverlauf und imitiert deinen Schreibstil."
        )
        
        logger.info(
            f"Import completed for chat {chat_id}: "
            f"{len(user_messages)} user, {len(other_messages)} other messages"
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
    
    def _save_state(self) -> None:
        """Save current bot state to storage."""
        try:
            self.storage.save_state(
                active_targets=self.active_targets,
                style_examples=self.llm.user_style_examples
            )
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
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
            logger.debug(f"Adding long pause: {extra_pause:.1f}s")
        
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
                logger.warning(f"Failed to send typing indicator: {e}")
                break
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming messages from targets with natural timing."""
        chat_id = update.effective_chat.id
        
        # Check if admin is in import mode - ignore non-forwarded messages
        if self._is_admin(update.effective_user.id) and context.user_data.get('import_mode', False):
            # In import mode, we only process forwarded messages
            # Non-forwarded messages are ignored (they'll be commands like /done)
            return
        
        # Only respond to active targets
        if chat_id not in self.active_targets:
            return
        
        user_message = update.message.text
        logger.info(f"[Chat {chat_id}] Message received: {user_message[:50]}...")
        
        # Small initial delay (reading the message)
        reading_delay = random.uniform(
            self.timing.get("reading_delay_min", 1.0),
            self.timing.get("reading_delay_max", 3.0)
        )
        await asyncio.sleep(reading_delay)
        
        # Get LLM response
        response = await self.llm.get_response(chat_id, user_message)
        
        # Calculate realistic typing delay
        typing_delay = self._calculate_typing_delay(response)
        logger.info(f"[Chat {chat_id}] Delay: {typing_delay:.1f}s for {len(response)} chars")
        
        # Show typing indicator while "composing" the message
        await self._send_typing_action(chat_id, typing_delay)
        
        # Send response
        await update.message.reply_text(response)
        logger.info(f"[Chat {chat_id}] Response sent: {response[:50]}...")
    
    async def run(self) -> None:
        """Start the bot."""
        logger.info(f"🚀 Bot starting as '{self.personality.get_name()}'...")
        logger.info(f"Admin User ID: {self.admin_user_id}")
        logger.info(f"Active targets: {len(self.active_targets)}")
        
        print(f"🚀 Bot startet als '{self.personality.get_name()}'...")
        print(f"Admin User ID: {self.admin_user_id}")
        print(f"Aktive Targets: {len(self.active_targets)}")
        
        try:
            # Initialize and start the application
            async with self.app:
                await self.app.start()
                await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
                
                # Keep the bot running until stopped
                stop_event = asyncio.Event()
                try:
                    await stop_event.wait()
                except (KeyboardInterrupt, SystemExit):
                    logger.info("Shutdown signal received")
                finally:
                    # Stop polling
                    await self.app.updater.stop()
                    await self.app.stop()
        finally:
            # Save state on shutdown
            logger.info("Saving state before shutdown...")
            self._save_state()
            logger.info("Bot shutdown complete")