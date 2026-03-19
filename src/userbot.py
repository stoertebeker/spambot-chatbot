"""Telegram Userbot for automatic spam responses."""
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from typing import Optional
import random

from .llm_handler import LLMHandler
from .personality import PersonalityManager
from .storage import BotStorage
from .timing_manager import TimingManager

logger = logging.getLogger(__name__)


class SpamResponderUserbot:
    """Userbot that automatically responds to whitelisted spammers."""
    
    def __init__(self, api_id: int, api_hash: str, session_string: Optional[str] = None):
        """Initialize the userbot.
        
        Args:
            api_id: Telegram API ID from my.telegram.org
            api_hash: Telegram API Hash from my.telegram.org
            session_string: Optional session string for persistent login
        """
        self.api_id = api_id
        self.api_hash = api_hash
        
        logger.info("Initializing Spam Responder Userbot...")
        
        # Initialize Telethon client
        session = StringSession(session_string) if session_string else StringSession()
        self.client = TelegramClient(session, api_id, api_hash)
        
        # Initialize storage
        self.storage = BotStorage()
        
        # Load saved state (whitelist instead of active_targets)
        self.whitelist, saved_style_examples = self.storage.load_state()
        logger.info(f"Loaded {len(self.whitelist)} whitelisted users from storage")
        
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
        
        # Paused state
        self.paused = False
        
        # My user ID (will be set on start)
        self.my_id = None
        
        # Register event handlers
        self._register_handlers()
        
        logger.info("Userbot initialization complete")
    
    def _register_handlers(self) -> None:
        """Register Telethon event handlers."""
        
        # Handle incoming private messages
        @self.client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
        async def handle_private_message(event):
            await self._handle_message(event)
        
        # Handle commands in Saved Messages (chat with yourself)
        @self.client.on(events.NewMessage(outgoing=True, pattern=r'^/'))
        async def handle_command(event):
            # Only handle commands in Saved Messages (chat with yourself)
            if not event.is_private:
                return
            if self.my_id and event.chat_id != self.my_id:
                return
            await self._handle_command(event)
    
    async def _handle_command(self, event) -> None:
        """Handle commands sent to Saved Messages."""
        text = event.message.text.strip()
        
        if text.startswith('/whitelist_add'):
            parts = text.split()
            if len(parts) != 2:
                await event.reply("❌ Usage: /whitelist_add <user_id>")
                return
            
            try:
                user_id = int(parts[1])
                self.whitelist.add(user_id)
                self._save_state()
                
                logger.info("="*80)
                logger.info("➕ WHITELIST ADD")
                logger.info(f"   User ID: {user_id}")
                logger.info(f"   Total whitelisted: {len(self.whitelist)}")
                logger.info("="*80)
                
                await event.reply(f"✅ User {user_id} added to whitelist!\nBot will now auto-respond.")
            except ValueError:
                await event.reply("❌ Invalid user ID!")
        
        elif text.startswith('/whitelist_remove'):
            parts = text.split()
            if len(parts) != 2:
                await event.reply("❌ Usage: /whitelist_remove <user_id>")
                return
            
            try:
                user_id = int(parts[1])
                if user_id in self.whitelist:
                    self.whitelist.remove(user_id)
                    self._save_state()
                    
                    logger.info("="*80)
                    logger.info("➖ WHITELIST REMOVE")
                    logger.info(f"   User ID: {user_id}")
                    logger.info(f"   Total whitelisted: {len(self.whitelist)}")
                    logger.info("="*80)
                    
                    await event.reply(f"✅ User {user_id} removed from whitelist!")
                else:
                    await event.reply(f"❌ User {user_id} not in whitelist.")
            except ValueError:
                await event.reply("❌ Invalid user ID!")
        
        elif text == '/whitelist_list':
            if not self.whitelist:
                await event.reply("📭 Whitelist is empty.")
                return
            
            whitelist_text = "\n".join(
                f"• {user_id} ({self.llm.get_conversation_length(user_id)} messages)"
                for user_id in self.whitelist
            )
            await event.reply(f"📋 Whitelisted users ({len(self.whitelist)}):\n\n{whitelist_text}")
        
        elif text == '/pause':
            self.paused = True
            logger.info("⏸️  Auto-responses PAUSED")
            await event.reply("⏸️ Auto-responses paused.\nUse /resume to continue.")
        
        elif text == '/resume':
            self.paused = False
            logger.info("▶️  Auto-responses RESUMED")
            await event.reply("▶️ Auto-responses resumed!")
        
        elif text == '/status':
            status_text = (
                f"🤖 Userbot Status\n\n"
                f"Persona: {self.personality.get_name()}\n"
                f"Model: {self.llm.model}\n"
                f"Whitelisted Users: {len(self.whitelist)}\n"
                f"Paused: {'Yes' if self.paused else 'No'}\n"
                f"Session: Active"
            )
            await event.reply(status_text)
        
        elif text.startswith('/import'):
            parts = text.split()
            if len(parts) != 2:
                await event.reply(
                    "❌ Usage: /import <user_id>\n\n"
                    "This will analyze your chat history with that user to learn your style."
                )
                return
            
            try:
                user_id = int(parts[1])
                await event.reply(f"📥 Importing chat history with user {user_id}...\nThis may take a moment.")
                
                # Fetch messages from the chat
                messages = []
                async for message in self.client.iter_messages(user_id, limit=100):
                    if message.text:
                        messages.append({
                            'text': message.text,
                            'outgoing': message.out,
                            'date': message.date
                        })
                
                # Reverse to get chronological order
                messages.reverse()
                
                # Separate your messages for style learning
                your_messages = [m['text'] for m in messages if m['outgoing']]
                their_messages = [m['text'] for m in messages if not m['outgoing']]
                
                # Add to LLM
                if your_messages:
                    self.llm.add_style_examples(user_id, your_messages[:10])
                
                # Build conversation history
                conversation = self.llm._get_conversation(user_id)
                for msg in messages[-20:]:  # Last 20 messages
                    role = "assistant" if msg['outgoing'] else "user"
                    conversation.append({"role": role, "content": msg['text']})
                
                await event.reply(
                    f"✅ Import complete!\n\n"
                    f"📊 Statistics:\n"
                    f"• Your messages: {len(your_messages)}\n"
                    f"• Their messages: {len(their_messages)}\n"
                    f"• Total: {len(messages)}\n\n"
                    f"Use /whitelist_add {user_id} to enable auto-responses."
                )
                
                logger.info(f"Imported {len(messages)} messages from user {user_id}")
                
            except ValueError:
                await event.reply("❌ Invalid user ID!")
            except Exception as e:
                logger.exception(f"Import failed: {e}")
                await event.reply(f"❌ Import failed: {e}")
        
        elif text == '/help':
            help_text = (
                "📖 Userbot Commands\n\n"
                "Send these commands in Saved Messages:\n\n"
                "/whitelist_add <id> - Add user to auto-respond\n"
                "/whitelist_remove <id> - Remove user\n"
                "/whitelist_list - Show all whitelisted\n"
                "/import <id> - Import chat history\n"
                "/pause - Pause auto-responses\n"
                "/resume - Resume auto-responses\n"
                "/status - Show bot status\n"
                "/help - Show this help"
            )
            await event.reply(help_text)
    
    async def _handle_message(self, event) -> None:
        """Handle incoming private messages."""
        sender = await event.get_sender()
        user_id = sender.id
        username = sender.username or "Unknown"
        message_text = event.message.text
        
        # LOG: Incoming message
        logger.info("="*80)
        logger.info("📨 INCOMING MESSAGE")
        logger.info(f"   User ID: {user_id}")
        logger.info(f"   Username: @{username}")
        logger.info(f"   Message: {message_text}")
        logger.info(f"   Whitelisted: {user_id in self.whitelist}")
        logger.info(f"   Paused: {self.paused}")
        logger.info("="*80)
        
        # Check if paused
        if self.paused:
            logger.info("⏭️  Ignoring message - Bot is paused")
            return
        
        # Check whitelist
        if user_id not in self.whitelist:
            logger.info(f"⏭️  Ignoring message - User {user_id} not whitelisted")
            return
        
        # Small reading delay
        reading_delay = random.uniform(
            self.timing.get("reading_delay_min", 1.0),
            self.timing.get("reading_delay_max", 3.0)
        )
        logger.info(f"⏱️  Reading delay: {reading_delay:.2f}s")
        await asyncio.sleep(reading_delay)
        
        # Get LLM response
        logger.info("🤖 Requesting LLM response...")
        response = await self.llm.get_response(user_id, message_text)
        
        # Calculate typing delay
        typing_delay = self._calculate_typing_delay(response)
        logger.info(f"⏱️  Typing delay: {typing_delay:.1f}s for {len(response)} chars")
        
        # Show typing indicator
        async with self.client.action(user_id, 'typing'):
            await asyncio.sleep(typing_delay)
        
        # Send response
        await self.client.send_message(user_id, response)
        
        # LOG: Outgoing message
        logger.info("="*80)
        logger.info("📤 OUTGOING MESSAGE")
        logger.info(f"   User ID: {user_id}")
        logger.info(f"   Response: {response}")
        logger.info(f"   Length: {len(response)} chars")
        logger.info("="*80)
    
    def _calculate_typing_delay(self, text: str) -> float:
        """Calculate realistic typing delay based on message length."""
        base_delay = len(text) / self.chars_per_second
        variation = random.uniform(0.8, 1.3)
        delay = base_delay * variation
        delay = max(self.min_delay, min(self.max_delay, delay))
        
        if random.random() < self.occasional_long_pause_chance:
            extra_pause = random.uniform(*self.long_pause_duration)
            delay += extra_pause
            logger.debug(f"Adding long pause: {extra_pause:.1f}s")
        
        return delay
    
    def _save_state(self) -> None:
        """Save current state to storage."""
        try:
            self.storage.save_state(
                active_targets=self.whitelist,  # Still uses same param name internally
                style_examples=self.llm.user_style_examples
            )
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    async def start(self) -> str:
        """Start the userbot and return session string.
        
        Returns:
            Session string for future logins
        """
        logger.info("🚀 Starting userbot...")
        
        await self.client.start()
        
        # Get session string for saving
        session_string = self.client.session.save()
        
        # Get my user info
        me = await self.client.get_me()
        self.my_id = me.id  # Store my ID for command filtering
        
        logger.info(f"✅ Logged in as: {me.first_name} (@{me.username})")
        logger.info(f"User ID: {me.id}")
        logger.info(f"Whitelisted users: {len(self.whitelist)}")
        
        print("="*60)
        print("✅ Userbot started successfully!")
        print(f"Logged in as: {me.first_name} (@{me.username})")
        print(f"Whitelisted users: {len(self.whitelist)}")
        print("="*60)
        print("\n💡 Send commands to 'Saved Messages' to control the bot:")
        print("   /help - Show all commands")
        print("   /whitelist_add <user_id> - Add a user")
        print("   /status - Check bot status")
        print("\n⚠️  Press Ctrl+C to stop")
        print("="*60)
        
        return session_string
    
    async def run(self) -> None:
        """Run the userbot until stopped."""
        try:
            # Start the client
            session_string = await self.start()
            
            # Save session string to storage
            self.storage.save_session(session_string)
            logger.info("Session string saved to storage")
            
            # Keep running
            await self.client.run_until_disconnected()
            
        except KeyboardInterrupt:
            logger.info("Userbot stopped by user")
            print("\n👋 Userbot stopped")
        except Exception as e:
            logger.exception(f"Userbot error: {e}")
            raise
        finally:
            # Save state on shutdown
            logger.info("Saving state before shutdown...")
            self._save_state()
            logger.info("Userbot shutdown complete")
    
    async def stop(self) -> None:
        """Stop the userbot gracefully."""
        logger.info("Stopping userbot...")
        self._save_state()
        await self.client.disconnect()
        logger.info("Userbot stopped")