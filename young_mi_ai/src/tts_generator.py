import aiohttp
import logging
import uuid
import json
import tempfile
import os

class TTSGenerator:
    def __init__(self, config):
        self.api_url = config.get('indextts_api_url')
        self.voice_ref = config.get('voice_reference_name')
        self.session = aiohttp.ClientSession()

    async def generate_audio_file(self, text):
        """
        Sends text to the IndexTTS API and saves the returned audio to a temporary file.
        Returns the path to the generated audio file.
        """
        if not self.api_url or not self.voice_ref:
            logging.error("IndexTTS API URL or voice reference name is not configured.")
            return None

        # IndexTTS API expects form data, not JSON
        data = aiohttp.FormData()
        data.add_field('text', text)
        data.add_field('voice', self.voice_ref)

        try:
            logging.info(f"Sending IndexTTS request for text: '{text}'")
            async with self.session.post(self.api_url, data=data) as response:
                if response.status == 200:
                    # Save the audio content to a temporary file in an OS-agnostic way
                    audio_data = await response.read()

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                        temp_file.write(audio_data)
                        temp_filename = temp_file.name

                    logging.info(f"Successfully generated temporary audio file at {temp_filename}")
                    return temp_filename
                else:
                    error_text = await response.text()
                    logging.error(f"Error from IndexTTS API: {response.status} - {error_text}")
                    return None

        except aiohttp.ClientConnectorError as e:
            logging.error(f"Could not connect to IndexTTS API at {self.api_url}. Is it running? Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while contacting IndexTTS: {e}")
            return None

    async def close_session(self):
        """Closes the aiohttp session."""
        await self.session.close()