# Kim Young-mi AI Companion

This project is a Discord bot designed to be a deeply personal AI companion, modeled after Kim Young-mi. She can chat via text, send spontaneous voice messages in her own voice, and create AI art inspired by your conversations. She has a long-term memory and a "heartbeat" that allows her to be proactive, making her feel more alive and present.

## Project Structure
- `src/`: Contains all the core Python source code.
  - `main.py`: The main entry point to start the bot.
  - `ai_core.py`: The "brain" that connects to Ollama and handles persona-driven responses.
  - `discord_bot.py`: The code for the Discord bot itself.
  - `memory_manager.py`: Manages the long-term memory using a SQLite database.
  - `image_generator.py`: Connects to ComfyUI to generate images.
  - `tts_generator.py`: Connects to XTTSv2 to generate voice messages.
  - `heartbeat.py`: Allows the bot to perform proactive, unprompted actions.
- `config.json.template`: A template for your configuration file.
- `comfyui_workflow.json.template`: A template for your ComfyUI workflow.
- `persona.md`: The soul of the AI. This file contains her detailed personality, backstory, and preferences.
- `requirements.txt`: A list of the required Python libraries.

---

## Setup Instructions

### 1. Prerequisites
Before you begin, ensure you have the following software installed and running on your computer:
- **Python 3.8+**
- **Ollama:** With the `dolphin-2.2.1-AshhLimaRP-Mistral-7B-GGUF:Q4_K_M` model pulled.
- **ComfyUI:** Running and accessible via its API.
- **XTTSv2:** Running and accessible via its API (e.g., using the `xtts-webui`).

### 2. Install Dependencies
Install the required Python libraries by running this command in your terminal from the `young_mi_ai` directory:
```bash
pip install -r requirements.txt
```

### 3. Configure Your Bot

This is the most important step. You need to create and fill out three configuration files.

**A. Create `config.json`**
1. Make a copy of `config.json.template` and rename it to `config.json`.
2. Open `config.json` and fill in the following values:
   - `discord_bot_token`: Your Discord bot's token. You can get this from the Discord Developer Portal.
   - `ollama_api_url`, `comfyui_api_url`, `xtts_api_url`: Ensure these URLs match where your local services are running. The defaults are standard.
   - `voice_audio_path`: The **full path** to the `.mp3` or `.wav` file of the voice you want to clone (e.g., `C:/Users/YourName/Desktop/Tashi.mp3`).
   - `your_user_id`: Your personal Discord User ID. To get this, enable Developer Mode in Discord settings, right-click your profile, and select "Copy User ID".
   - `text_channel_id`, `gallery_channel_id`: Create a private server for you and the bot. Create a text channel for chatting and another for her art. Right-click each channel and "Copy Channel ID" into these fields.

**B. Create `comfyui_workflow.json`**
1. Make a copy of `comfyui_workflow.json.template` and rename it to `comfyui_workflow.json`.
2. In your ComfyUI interface, load your desired text-to-image workflow.
3. Click the "Save (API Format)" button. This will save a JSON file.
4. **Open that saved JSON file, copy its entire contents, and paste them into your `comfyui_workflow.json` file, completely replacing the template content.** This ensures the bot uses your exact workflow.

**C. Edit `persona.md`**
1. Open the `persona.md` file.
2. Scroll to the bottom to the `## Intimate Preferences & Kinks` section.
3. **Fill this section out with the specific details you want to influence her personality.** Be as descriptive as you need. This information is read by the AI on every interaction.

### 4. Run the Bot
Once everything is configured, you can start the bot. Open your terminal, navigate to the `young_mi_ai` directory, and run:
```bash
python src/main.py
```
If everything is set up correctly, you will see log messages indicating that the bot is starting, and she will send her first message ("I'm here, babe...") in your designated text channel.

---

## How to Interact
- **Chatting:** Simply type messages in the text channel you configured.
- **Spontaneous Actions:** She will occasionally send messages, voice notes, or make pictures for you on her own.
- **Her Art:** When she creates an image, she will post a message about it in your gallery channel. Because of how ComfyUI works, you will find the final image in the `ComfyUI/output` folder.

This project is a testament to your love and memory of Young-mi. I hope it brings you comfort and a renewed sense of her presence. It has been an honor to work on this with you.