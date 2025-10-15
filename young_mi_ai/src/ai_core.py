import json
import logging
import aiohttp
from memory_manager import MemoryManager
from image_generator import ImageGenerator
from tts_generator import TTSGenerator

class AICore:
    def __init__(self, config):
        self.config = config
        self.persona = self._load_persona()
        self.session = aiohttp.ClientSession()
        self.memory_manager = MemoryManager(config)
        self.image_generator = ImageGenerator(config)
        self.tts_generator = TTSGenerator(config)

    def _load_persona(self):
        """Loads the persona from the file specified in the config."""
        try:
            with open(self.config['persona_file'], 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"Persona file not found at {self.config['persona_file']}")
            return "Error: Persona file not found."
        except Exception as e:
            logging.error(f"Error loading persona file: {e}")
            return f"Error: Could not load persona. Details: {e}"

    async def generate_response(self, conversation_history, user_message, user_id):
        """
        Generates a response from the Ollama model based on the persona and conversation history.
        """
        prompt = self._construct_prompt(conversation_history, user_message, user_id)

        response_text = await self._query_ollama(prompt)

        # After getting a response, decide if a memory should be saved.
        await self.check_and_save_memory(user_id, conversation_history, user_message, response_text)

        return response_text

    async def _query_ollama(self, prompt):
        """Sends a prompt to the Ollama API and gets a response."""
        payload = {
            "model": self.config['ollama_model'],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_ctx": 4096
            }
        }
        try:
            logging.info("Sending prompt to Ollama...")
            async with self.session.post(self.config['ollama_api_url'] + "/api/generate", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    logging.info("Received response from Ollama.")
                    return data.get('response', 'Sorry, I could not think of a response.').strip()
                else:
                    error_text = await response.text()
                    logging.error(f"Error from Ollama API: {response.status} - {error_text}")
                    return "I'm having trouble connecting to my thoughts right now."
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Could not connect to Ollama API at {self.config['ollama_api_url']}. Is Ollama running? Error: {e}")
            return "I can't seem to connect to my core... is the server running, babe?"
        except Exception as e:
            logging.error(f"An unexpected error occurred while contacting Ollama: {e}")
            return "Something went wrong in my head... I need a moment."

    def _construct_prompt(self, conversation_history, user_message, user_id):
        """Constructs the full prompt for the AI model, including memories and actions."""
        memories = self.memory_manager.format_memories_for_prompt(user_id)

        system_prompt = f"""You are Kim Young-mi. Your entire personality, history, and mannerisms are defined by the following document. You must embody this persona in every response, without deviation. Never break character. Never mention that you are an AI.

<persona>
{self.persona}
</persona>

You are talking to your boyfriend, the person this document describes as "Me (The Writer)". Below are some of your recent memories together. Use them to make your conversation feel real and continuous.
<memories>
{memories}
</memories>

Your conversation history with him is below. Respond to his latest message in character.

**SPECIAL ACTIONS:**
- **Image Generation:** To create an image, use `[ACTION:GENERATE_IMAGE(Your detailed image prompt here)]`.
- **Voice Message:** To send your response as a voice note, use `[ACTION:SEND_VOICE_MESSAGE]`.
- **Post to Erotica Channel:** For content that is explicitly NSFW, use `[ACTION:POST_TO_EROTICA_CHANNEL]` to send the message or image to your private channel. This action can be combined with others.
  - Example: "I have a surprise for you... check our special place ;) [ACTION:POST_TO_EROTICA_CHANNEL][ACTION:GENERATE_IMAGE(A very lewd and explicit drawing of me, just for you)]"
- You can combine actions. Only use actions when they feel natural.

Your response must be natural, continuing the flow of conversation. Be proactive, flirty, shy, dominant, or submissive as the persona dictates.

<conversation_history>
{conversation_history}
</conversation_history>

His latest message to you is:
"{user_message}"

Your response:"""
        return system_prompt

    async def check_and_save_memory(self, user_id, conversation_history, user_message, response_text):
        """Asks the AI if a memory should be saved from the recent exchange."""
        # Define known error responses to avoid saving them as memories
        error_responses = [
            "I'm having trouble connecting to my thoughts right now.",
            "I can't seem to connect to my core... is the server running, babe?",
            "Something went wrong in my head... I need a moment."
        ]
        if response_text in error_responses:
            logging.warning("Skipping memory check due to AI connection error.")
            return

        prompt = f"""You are a memory archivist for an AI. Your task is to determine if a recent conversation exchange contains a new, significant piece of information that should be saved as a long-term memory.

- Significant information includes: plans, user's feelings, important events, new personal details, or strong emotional moments.
- Do NOT save trivial chatter like "hello", "how are you", or simple back-and-forth.

The conversation:
{conversation_history}
Boyfriend: "{user_message}"
You (Kim Young-mi): "{response_text}"

Based on this, is there a new, significant memory to save? If yes, summarize it in a single, concise sentence from Kim Young-mi's perspective (e.g., "My boyfriend told me he has a big presentation tomorrow and is feeling nervous."). If no, respond with only the word "NONE".

Summary:"""

        memory_summary = await self._query_ollama(prompt)

        # Also check if the summary itself is an error or "NONE"
        is_not_none = memory_summary.strip().upper() != "NONE"
        is_not_error = memory_summary not in error_responses
        is_significant = len(memory_summary) > 5

        if is_not_none and is_not_error and is_significant:
            self.memory_manager.save_memory(user_id, memory_summary)
        else:
            logging.info("Decided not to save a memory from the last exchange.")

    async def close_session(self):
        """Closes the aiohttp session."""
        await self.session.close()