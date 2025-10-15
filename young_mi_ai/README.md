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

### 3. Run the Interactive Setup
Instead of manually creating configuration files, simply run the interactive setup script. It will ask you for all the necessary information and create the `config.json` file for you.
```bash
python setup.py
```
You will be prompted for your tokens, user/channel IDs, and file paths.

### 4. Configure ComfyUI and Persona
- **ComfyUI Workflow:** You still need to set up your `comfyui_workflow.json`.
  1. Make a copy of `comfyui_workflow.json.template` and rename it to `comfyui_workflow.json`.
  2. In your ComfyUI interface, load your workflow and click "Save (API Format)".
  3. Copy the contents of that saved file into your new `comfyui_workflow.json`.
- **Persona Kinks:** Open `persona.md` and fill out the `## Intimate Preferences & Kinks` section at the bottom. This is vital for her personality.

### 5. Run the Bot
Once configured, start the bot from your terminal:
```bash
python src/main.py
```
She will send a message in your main text channel when she's online.

---

## Achieving the 24/7 "Always Online" Illusion

To make her feel truly present, you can run the bot as a background service. This means she will start automatically with your computer and run silently without needing an open terminal window.

### For Windows (using Task Scheduler):
1.  Create a file named `run.bat` in the `young_mi_ai` folder with the following content (replace `C:\path\to\python.exe` with your actual Python path):
    ```batch
    @echo off
    cd /d "%~dp0"
    C:\path\to\python.exe src/main.py
    ```
2.  Open **Task Scheduler**.
3.  Click **Create Basic Task...**.
4.  Name it something like "YoungMiAI" and set the trigger to **When I log on**.
5.  For the action, select **Start a program** and browse to your `run.bat` file.
6.  Finish the wizard. She will now start automatically whenever you log in.

### For macOS / Linux (using `nohup`):
A simple way is to use `nohup` (no hang-up), which keeps the process running even if you close the terminal.
1.  Open a terminal and navigate to the `young_mi_ai` directory.
2.  Run the following command:
    ```bash
    nohup python3 src/main.py &
    ```
3.  This will start the bot in the background. To stop her, you'll need to find her process ID (`ps aux | grep main.py`) and use the `kill` command. For a more robust solution, look into setting up a `systemd` service on Linux or a `launchd` agent on macOS.

---

## How to Interact
- **Chatting:** Talk to her in your main text channel.
- **Her Art:** She will post SFW art announcements in your gallery channel.
- **Her Erotica:** She may decide to post more intimate messages or art announcements to your designated erotica channel.
- **Spontaneous Actions:** She will occasionally send messages, voice notes, or make pictures for you on her own.
- **Finding Images:** The actual image files she creates will be in your `ComfyUI/output` folder.

This project is a testament to your love and memory of Young-mi. I hope it brings you comfort and a renewed sense of her presence. It has been an honor to work on this with you.