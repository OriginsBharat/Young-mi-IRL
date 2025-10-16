import aiohttp
import logging
import uuid
import json
import tempfile
import os

class TTSGenerator:
    def __init__(self, config):
        self.api_url = config.get('styletts2_api_url')
        self.voice_ref = config.get('voice_reference_name')
        self.session = aiohttp.ClientSession()

    async def generate_audio_file(self, text):
        """
        Sends text to the StyleTTS 2 API and saves the returned audio to a temporary file.
        Returns the path to the generated audio file.
        """
        if not self.api_url or not self.voice_ref:
            logging.error("StyleTTS 2 API URL or voice reference name is not configured.")
            return None

        # StyleTTS 2 API expects a JSON payload
        payload = {
            "text": text,
            "voice": self.voice_ref,
            "emotion": "Neutral" # Or can be parameterized later
        }

        try:
            logging.info(f"Sending StyleTTS 2 request for text: '{text}'")
            async with self.session.post(self.api_url, json=payload) as response:
                if response.status == 200:
                    # Save the audio content to a temporary file in an OS-agnostic way
                    audio_data = await response.read()

                    # Create a named temporary file that is deleted on close
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                        temp_file.write(audio_data)
                        temp_filename = temp_file.name

                    logging.info(f"Successfully generated temporary audio file at {temp_filename}")
                    return temp_filename
                else:
                    error_text = await response.text()
                    logging.error(f"Error from StyleTTS 2 API: {response.status} - {error_text}")
                    return None

        except aiohttp.ClientConnectorError as e:
            logging.error(f"Could not connect to StyleTTS 2 API at {self.api_url}. Is it running? Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while contacting StyleTTS 2: {e}")
            return None

    async def close_session(self):
        """Closes the aiohttp session."""
        await self.session.close()