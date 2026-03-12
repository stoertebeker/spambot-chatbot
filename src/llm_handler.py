"""LLM Handler using LiteLLM for flexible model support."""
import os
import time
import logging
from typing import List, Dict, Optional, Tuple
from litellm import completion
from litellm.exceptions import (
    RateLimitError,
    APIError,
    Timeout,
    ServiceUnavailableError
)

logger = logging.getLogger(__name__)


class LLMHandler:
    """Handles LLM interactions via LiteLLM."""
    
    def __init__(self, model: str = None, system_prompt: str = None, max_retries: int = 3):
        self.model = model or os.getenv("LITELLM_MODEL", "gpt-3.5-turbo")
        self.system_prompt = system_prompt or "Du bist ein hilfreicher Assistent."
        self.conversation_history: Dict[int, List[Dict[str, str]]] = {}
        self.user_style_examples: Dict[int, List[str]] = {}  # Store user's writing style
        self.max_retries = max_retries
        
        # Set LiteLLM API base if provided
        if os.getenv("LITELLM_API_BASE"):
            os.environ["LITELLM_API_BASE"] = os.getenv("LITELLM_API_BASE")
            logger.info(f"Using custom LiteLLM API base: {os.getenv('LITELLM_API_BASE')}")
        
        # Set API key if provided (LiteLLM will use it)
        if os.getenv("LITELLM_API_KEY"):
            os.environ["LITELLM_API_KEY"] = os.getenv("LITELLM_API_KEY")
            logger.info("LiteLLM API key configured")
        
        logger.info(f"LLM Handler initialized with model: {self.model}")
        
    def _get_conversation(self, chat_id: int) -> List[Dict[str, str]]:
        """Get or create conversation history for a chat."""
        if chat_id not in self.conversation_history:
            system_content = self.system_prompt
            
            # If we have user style examples, add them to system prompt
            if chat_id in self.user_style_examples and self.user_style_examples[chat_id]:
                style_examples = "\n".join(self.user_style_examples[chat_id])
                system_content += (
                    f"\n\nWICHTIG: Der Nutzer, den du imitierst, hat in der Vergangenheit "
                    f"so geschrieben (ahme diesen Stil nach):\n{style_examples}"
                )
            
            self.conversation_history[chat_id] = [
                {"role": "system", "content": system_content}
            ]
        return self.conversation_history[chat_id]
    
    async def get_response(self, chat_id: int, user_message: str) -> str:
        """Generate a response using LiteLLM with retry logic.
        
        Args:
            chat_id: Telegram chat ID
            user_message: User's message
            
        Returns:
            LLM's response
        """
        logger.info(f"🧠 LLM Request for chat {chat_id}")
        logger.info(f"   User message: {user_message}")
        
        # Get conversation history
        messages = self._get_conversation(chat_id)
        logger.info(f"   Conversation length: {len(messages)} messages")
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        # Try to get response with retries
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"LLM request attempt {attempt + 1}/{self.max_retries}")
                
                # Get completion from LiteLLM
                response = completion(
                    model=self.model,
                    messages=messages,
                    temperature=0.8,  # Etwas kreativere Antworten
                    max_tokens=150  # Kürzere Antworten (1-2 Sätze)
                )
                
                # Extract response
                assistant_message = response.choices[0].message.content
                
                # Add to history
                messages.append({"role": "assistant", "content": assistant_message})
                
                # Limit conversation history to last 20 messages (+ system prompt)
                if len(messages) > 21:
                    self.conversation_history[chat_id] = [messages[0]] + messages[-20:]
                
                logger.info(f"✅ LLM response generated successfully")
                logger.info(f"   Model: {self.model}")
                logger.info(f"   Response length: {len(assistant_message)} chars")
                logger.info(f"   Response: {assistant_message}")
                return assistant_message
                
            except RateLimitError as e:
                logger.warning(f"Rate limit error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries reached for rate limit")
                    return "Entschuldigung, zu viele Anfragen gerade. Versuch's gleich nochmal! 😅"
            
            except Timeout as e:
                logger.warning(f"Timeout error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error("Max retries reached for timeout")
                    return "Entschuldigung, das dauert gerade zu lange. Kannst du das wiederholen? 🤔"
            
            except ServiceUnavailableError as e:
                logger.warning(f"Service unavailable (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error("Max retries reached for service unavailable")
                    return "Hmm, irgendwas klappt gerade nicht. Versuchen wir's später nochmal? 😊"
            
            except APIError as e:
                logger.error(f"API error: {e}")
                return "Entschuldigung, da ist was schiefgelaufen. 😅"
            
            except Exception as e:
                logger.exception(f"Unexpected error in LLM request: {e}")
                return "Entschuldigung, ich habe gerade Schwierigkeiten zu antworten. 😅"
        
        # Should never reach here, but just in case
        return "Entschuldigung, ich habe gerade Schwierigkeiten zu antworten. 😅"
    
    def reset_conversation(self, chat_id: int) -> None:
        """Reset conversation history for a specific chat."""
        if chat_id in self.conversation_history:
            del self.conversation_history[chat_id]
        logger.info(f"Conversation reset for chat {chat_id}")
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt."""
        self.system_prompt = prompt
        # Reset all conversations to use new prompt
        self.conversation_history.clear()
    
    def get_conversation_length(self, chat_id: int) -> int:
        """Get number of messages in conversation."""
        if chat_id in self.conversation_history:
            return len(self.conversation_history[chat_id]) - 1  # Exclude system prompt
        return 0
    
    def add_style_examples(self, chat_id: int, examples: List[str]) -> None:
        """Add examples of user's writing style for this chat.
        
        Args:
            chat_id: Telegram chat ID
            examples: List of example messages from the user
        """
        if chat_id not in self.user_style_examples:
            self.user_style_examples[chat_id] = []
        
        self.user_style_examples[chat_id].extend(examples)
        
        # Keep only last 10 examples
        if len(self.user_style_examples[chat_id]) > 10:
            self.user_style_examples[chat_id] = self.user_style_examples[chat_id][-10:]
        
        # Reset conversation to apply new style
        if chat_id in self.conversation_history:
            del self.conversation_history[chat_id]
        
        logger.info(f"Style examples added for chat {chat_id}: {len(examples)} messages")
    
    def get_style_examples(self, chat_id: int) -> List[str]:
        """Get stored style examples for a chat."""
        return self.user_style_examples.get(chat_id, [])
    
    async def analyze_user_style(self, messages: List[str]) -> str:
        """Analyze user's writing style using LLM.
        
        Args:
            messages: List of user messages to analyze
            
        Returns:
            Analysis of writing style
        """
        if not messages:
            return "Keine Nachrichten zum Analysieren."
        
        analysis_prompt = (
            "Analysiere den Schreibstil der folgenden Nachrichten. "
            "Beschreibe kurz: Satzlänge, Emoji-Verwendung, Formalität, "
            "typische Ausdrücke, Grammatik-Eigenheiten.\n\n"
            "Nachrichten:\n"
        )
        
        for i, msg in enumerate(messages[:10], 1):
            analysis_prompt += f"{i}. {msg}\n"
        
        try:
            logger.info("Analyzing user writing style...")
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du bist ein Experte für Sprachstil-Analyse."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            analysis = response.choices[0].message.content
            logger.info("Style analysis completed")
            return analysis
        except Exception as e:
            logger.exception(f"Error in style analysis: {e}")
            return f"Fehler bei der Analyse: {e}"