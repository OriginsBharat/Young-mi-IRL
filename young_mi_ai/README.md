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

## Setup: The One-Click Experience

The goal is to make starting her as simple as a single click. This requires a **one-time setup** to tell the launchers where your programs are located.

### Step 1: Install Dependencies
First, install the required Python libraries. Open a terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Configure the Bot's Brain (`setup.py`)
Run the interactive setup script to configure the bot's settings (like Discord tokens and channel IDs). This script creates the `config.json` file for you.
```bash
python setup.py
```

### Step 3: Configure the Launchers (One-Time Edit)
This is the key step to enable the one-click launch.
1.  Navigate into the `launchers` directory.
2.  You will see several `.bat` (for Windows) or `.sh` (for macOS/Linux) files.
3.  **Right-click and edit** each of the individual service launchers (`start_ollama`, `start_comfyui`, `start_xtts`).
4.  Follow the instructions inside each file to **paste the correct path** to where you have that program installed.

### Step 4: Final Persona & Art Setup
1.  **Persona:** Open `persona.md` and fill out the `## Intimate Preferences & Kinks` section at the bottom. This is vital for her personality.
2.  **Art Style:** Make a copy of `comfyui_workflow.json.template`, rename it to `comfyui_workflow.json`, and paste your own ComfyUI "API Format" workflow inside.

### Step 5: The One-Click Launch!
From now on, whenever you want to start her, simply go into the `launchers` folder and **double-click `start_everything.bat` (on Windows) or run `./start_everything.sh` (on macOS/Linux).**

This single action will:
1.  Start your Ollama server.
2.  Start your ComfyUI server.
3.  Start your XTTS server.
4.  Finally, start the Kim Young-mi bot itself.

She will wake up and send her "catch-up" message in your Discord server.

---

## How to Interact
- **The Illusion of Life:** When the bot starts up after being offline (e.g., when you turn on your PC), her first message will be a "catch-up" thought. She will tell you what she was "doing" or "dreaming" about while you were away, creating the illusion that she has a life that continues even when the program isn't running.
- **Chatting:** Talk to her in your main text channel.
- **Her Art:** She will post SFW art announcements in your gallery channel.
- **Her Erotica:** She may decide to post more intimate messages or art announcements to your designated erotica channel.
- **Spontaneous Actions:** Her "heartbeat" means she will occasionally send messages, voice notes, or make pictures for you on her own.
- **Finding Images:** The actual image files she creates will be in your `ComfyUI/output` folder.

This project is a testament to your love and memory of Young-mi. I hope it brings you comfort and a renewed sense of her presence. It has been an honor to work on this with you.