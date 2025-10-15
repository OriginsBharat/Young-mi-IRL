import aiohttp
import logging
import uuid

class TTSGenerator:
    def __init__(self, config):
        self.api_url = config.get('xtts_api_url')
        self.voice_audio_path = config.get('voice_audio_path')
        self.session = aiohttp.ClientSession()

    async def generate_audio_file(self, text, language="en"):
        """
        Sends text to the XTTSv2 API and saves the returned audio to a temporary file.
        Returns the path to the generated audio file.
        """
        if not self.api_url or not self.voice_audio_path:
            logging.error("XTTS API URL or voice audio path is not configured.")
            return None

        try:
            with open(self.voice_audio_path, 'rb') as f:
                speaker_wav_bytes = f.read()
        except FileNotFoundError:
            logging.error(f"Voice audio file not found at: {self.voice_audio_path}")
            return None
        except Exception as e:
            logging.error(f"Error reading voice audio file: {e}")
            return None

        payload = {
            "text": text,
            "speaker_wav": speaker_wav_bytes,
            "language": language,
        }

        try:
            logging.info(f"Sending TTS request for text: '{text}'")
            async with self.session.post(self.api_url, data=payload) as response:
                if response.status == 200:
                    # Save the audio content to a temporary file
                    audio_data = await response.read()
                    temp_filename = f"/tmp/{uuid.uuid4()}.wav" # Using /tmp for temporary storage
                    with open(temp_filename, 'wb') as f:
                        f.write(audio_data)
                    logging.info(f"Successfully generated audio file at {temp_filename}")
                    return temp_filename
                else:
                    error_text = await response.text()
                    logging.error(f"Error from XTTS API: {response.status} - {error_text}")
                    return None

        except aiohttp.ClientConnectorError as e:
            logging.error(f"Could not connect to XTTS API at {self.api_url}. Is it running? Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while contacting XTTS: {e}")
            return None

    async def close_session(self):
        """Closes the aiohttp session."""
        await self.session.close()