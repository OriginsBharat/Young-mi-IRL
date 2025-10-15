import asyncio
import logging
import random

class Heartbeat:
    def __init__(self, config, bot, ai_core):
        self.bot = bot
        self.ai_core = ai_core
        self.config = config
        self._task = None
        # Proactive action settings
        self.min_interval_seconds = 60 * 15 # 15 minutes
        self.max_interval_seconds = 60 * 90 # 90 minutes
        self.action_probability = 0.4 # 40% chance of acting per interval

    async def start(self):
        """Starts the heartbeat loop as a background task."""
        if self._task is None:
            self._task = asyncio.create_task(self._run())
            logging.info("Heartbeat started. Young-mi is now thinking on her own.")

    async def stop(self):
        """Stops the heartbeat loop."""
        if self._task:
            self._task.cancel()
            self._task = None
            logging.info("Heartbeat stopped.")

    async def _run(self):
        """The main loop for the heartbeat."""
        await self.bot.wait_until_ready() # Ensure the bot is connected first
        logging.info("Heartbeat loop is now active.")

        while not self.bot.is_closed():
            try:
                # Wait for a random interval
                interval = random.uniform(self.min_interval_seconds, self.max_interval_seconds)
                logging.info(f"Heartbeat: Next check in {interval/60:.2f} minutes.")
                await asyncio.sleep(interval)

                # Decide if we should perform an action
                if random.random() < self.action_probability:
                    logging.info("Heartbeat: Triggering a proactive action.")
                    await self._perform_proactive_action()
                else:
                    logging.info("Heartbeat: Decided to stay quiet this time.")

            except asyncio.CancelledError:
                logging.info("Heartbeat task was cancelled.")
                break
            except Exception as e:
                logging.error(f"An error occurred in the heartbeat loop: {e}", exc_info=True)
                # Wait a bit before retrying to avoid spamming errors
                await asyncio.sleep(60)

    async def _perform_proactive_action(self):
        """Generates and sends a proactive message."""
        try:
            # A special prompt for the AI to generate a spontaneous thought
            proactive_prompt = "You are Kim Young-mi. You've been quiet for a while and are thinking about your boyfriend. What do you want to say or do? You could send him a message, a voice note, or even make a picture for him. Be creative and stay in character."

            # This is a simplified context. A more advanced version could pull recent memories.
            response_text = await self.ai_core.generate_response(
                conversation_history="You have been quiet for a while.",
                user_message=proactive_prompt, # We use the user_message field for the instruction
                user_id=str(self.config['your_user_id'])
            )

            text_channel = self.bot.get_channel(int(self.config['text_channel_id']))
            if text_channel:
                logging.info(f"Heartbeat: Sending proactive message: {response_text}")
                # The existing handler will parse for actions (voice, image)
                await self.bot._handle_response(text_channel, response_text)
            else:
                logging.error("Heartbeat: Could not find the text channel to send proactive message.")

        except Exception as e:
            logging.error(f"Failed to perform proactive action: {e}", exc_info=True)