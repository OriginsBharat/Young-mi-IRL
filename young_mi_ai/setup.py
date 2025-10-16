import json
import os

def interactive_setup():
    """
    Guides the user through an interactive setup process to create the config.json file.
    """
    print("--- Kim Young-mi AI Companion Setup ---")
    print("I'll ask you a few questions to get everything set up.")
    print("You can find most of these values in your Discord server by enabling Developer Mode.\n")

    config = {}

    # --- Get required values ---
    config['discord_bot_token'] = input("Enter your Discord Bot Token: ").strip()
    config['your_user_id'] = input("Enter your personal Discord User ID: ").strip()
    config['text_channel_id'] = input("Enter the ID of your main text channel: ").strip()
    config['gallery_channel_id'] = input("Enter the ID of the channel for her art: ").strip()
    config['erotica_channel_id'] = input("Enter the ID of the channel for her erotic content: ").strip()
    config['voice_channel_id'] = input("Enter the ID of the voice channel for calls (can be the same as text channel): ").strip()

    config['voice_reference_name'] = input("Enter the filename of her voice (e.g., Tashi.mp3): ").strip()

    # --- Get optional values with defaults ---
    print("\nNow for the API endpoints. The defaults are usually correct if you're running everything locally.")

    default_ollama = "http://localhost:11434"
    config['ollama_api_url'] = input(f"Ollama API URL (default: {default_ollama}): ").strip() or default_ollama

    default_comfyui = "http://localhost:8188"
    config['comfyui_api_url'] = input(f"ComfyUI API URL (default: {default_comfyui}): ").strip() or default_comfyui

    default_styletts = "http://localhost:5000/tts"
    config['styletts2_api_url'] = input(f"StyleTTS 2 API URL (default: {default_styletts}): ").strip() or default_styletts

    # --- Add other static values ---
    config['ollama_model'] = "TheBloke/dolphin-2.2.1-AshhLimaRP-Mistral-7B-GGUF:Q4_K_M"
    config['persona_file'] = "persona.md"
    config['database_file'] = "memory.db"

    # --- Save the config file ---
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("\n✅ Setup complete! `config.json` has been created successfully.")
        print("You can now run the bot using: python src/main.py")
    except Exception as e:
        print(f"\n❌ An error occurred while saving the file: {e}")

if __name__ == "__main__":
    interactive_setup()