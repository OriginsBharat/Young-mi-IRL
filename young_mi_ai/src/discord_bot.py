import discord
import logging

class YoungMiBot(discord.Client):
    def __init__(self, config, ai_core, **options):
        super().__init__(**options)
        self.config = config
        self.ai_core = ai_core
        self.your_user_id = int(self.config['your_user_id'])
        self.text_channel_id = int(self.config['text_channel_id'])
        self.gallery_channel_id = int(self.config['gallery_channel_id'])
        self.erotica_channel_id = int(self.config.get('erotica_channel_id', 0))

import time
import json

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logging.info('Kim Young-mi is online.')

        text_channel = self.get_channel(self.text_channel_id)
        if not text_channel:
            logging.error(f"Cannot find text channel with ID {self.text_channel_id}. Cannot send welcome message.")
            return

        # Calculate offline duration and send dynamic welcome message
        try:
            with open('bot_state.json', 'r') as f:
                state = json.load(f)
                last_shutdown_time = state.get('last_shutdown_time', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            last_shutdown_time = 0

        current_time = time.time()
        offline_duration = current_time - last_shutdown_time if last_shutdown_time > 0 else 0

        # If offline for more than 2 minutes, generate a catch-up message.
        # Otherwise, it was probably just a quick restart.
        if offline_duration > 120:
            welcome_message = await self.ai_core.generate_catchup_message(offline_duration)
        else:
            welcome_message = "I'm back, babe."

        if welcome_message:
            await self._handle_response(text_channel, welcome_message)

import re

    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return

        # Only respond to you in the designated channel
        if message.author.id != self.your_user_id or message.channel.id != self.text_channel_id:
            return

        logging.info(f"Received message from you: '{message.content}'")

        try:
            async with message.channel.typing():
                history_messages = [msg async for msg in message.channel.history(limit=15)]
                history_messages.reverse()

                conversation_history = self._format_history(history_messages)

                raw_response = await self.ai_core.generate_response(
                    conversation_history=conversation_history,
                    user_message=message.content,
                    user_id=str(self.your_user_id)
                )

                # Handle potential actions in the response
                await self._handle_response(message.channel, raw_response)

        except Exception as e:
            logging.error(f"An error occurred while processing a message: {e}", exc_info=True)
            await message.channel.send("Ugh, my head hurts... I think something went wrong. Can you check the logs, babe?")

import os

    async def _handle_response(self, channel, response_text):
        """Parses the AI response for actions and sends messages accordingly."""
        text_to_send = response_text
        target_channel = channel # Default to the channel the message came from

        # --- Handle Erotica Channel Action ---
        post_to_erotica = '[ACTION:POST_TO_EROTICA_CHANNEL]' in text_to_send
        if post_to_erotica:
            text_to_send = text_to_send.replace('[ACTION:POST_TO_EROTICA_CHANNEL]', '').strip()
            erotica_channel_obj = self.get_channel(self.erotica_channel_id)
            if erotica_channel_obj:
                target_channel = erotica_channel_obj
            else:
                logging.warning(f"Erotica channel ID {self.erotica_channel_id} not found or not configured. Posting to default channel.")
                await channel.send("Babe, I wanted to post something to our special place, but I can't find the channel...")

        # --- Handle Voice Message Action ---
        send_as_voice = '[ACTION:SEND_VOICE_MESSAGE]' in text_to_send
        if send_as_voice:
            text_to_send = text_to_send.replace('[ACTION:SEND_VOICE_MESSAGE]', '').strip()

        # --- Handle Image Generation Action ---
        image_action_match = re.search(r'\[ACTION:GENERATE_IMAGE\((.*?)\)\]', text_to_send)
        if image_action_match:
            image_prompt = image_action_match.group(1)
            text_to_send = re.sub(r'\[ACTION:GENERATE_IMAGE\(.*?\)\]', '', text_to_send).strip()
            # Image generation messages always go to the gallery, but the text part respects the target channel
            await self._handle_image_generation(target_channel, image_prompt)

        # --- Send the final message (text or voice) ---
        if text_to_send:
            if send_as_voice:
                await self._send_voice_message(target_channel, text_to_send)
            else:
                await target_channel.send(text_to_send)

    async def _handle_image_generation(self, channel, prompt):
        """Handles the logic for generating and notifying about an image."""
        logging.info(f"AI requested an image with prompt: '{prompt}'")
        gallery_channel = self.get_channel(self.gallery_channel_id)
        if not gallery_channel:
            logging.error(f"Gallery channel with ID {self.gallery_channel_id} not found!")
            await channel.send("Babe, I wanted to make you a picture, but I can't find our gallery channel.")
            return

        await gallery_channel.send(f"I'm starting on that picture for you... The idea is: *'{prompt}'*")
        await self.ai_core.image_generator.generate_image(prompt)

    async def _send_voice_message(self, channel, text):
        """Generates audio and sends it as a voice message."""
        logging.info("Generating voice message...")
        audio_filepath = await self.ai_core.tts_generator.generate_audio_file(text)

        if audio_filepath:
            try:
                # Discord voice messages require the 'voice' flag to be set on the file.
                await channel.send(file=discord.File(audio_filepath, spoiler=False, description="Voice Message"))
                logging.info("Voice message sent successfully.")
            except Exception as e:
                logging.error(f"Failed to send voice message file: {e}")
                await channel.send("I tried to send you a voice note, but the file got corrupted or something...")
            finally:
                # Clean up the temporary audio file
                os.remove(audio_filepath)
        else:
            logging.error("Voice message generation failed.")
            await channel.send("I wanted to say something, but my voice is gone... The TTS isn't working, babe.")

    def _format_history(self, messages):
        """Formats a list of Discord messages into a string for the AI prompt."""
        formatted = []
        for msg in messages:
            name = "You" if msg.author.id == self.your_user_id else "Kim Young-mi"
            formatted.append(f"{name}: {msg.content}")
        return "\n".join(formatted)
