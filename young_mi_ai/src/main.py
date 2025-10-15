import asyncio
import json
import logging
import discord
from ai_core import AICore
from discord_bot import YoungMiBot
from heartbeat import Heartbeat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Loads the configuration from config.json."""
    try:
        with open("config.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("FATAL: config.json not found. Please copy config.json.template to config.json and fill in your details.")
        return None
    except json.JSONDecodeError:
        logging.error("FATAL: Error decoding config.json. Please ensure it is valid JSON.")
        return None
    except Exception as e:
        logging.error(f"FATAL: An unexpected error occurred loading config: {e}")
        return None

def main():
    """Main function to initialize and run the bot."""
    logging.info("Starting Kim Young-mi AI...")
    config = load_config()
    if not config:
        return

    # Initialize the AI Core
    ai_core = AICore(config)
    logging.info("AI Core and Memory Manager initialized.")

    # Setup Discord Bot Intents
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.guilds = True

    # Create the bot instance
    bot = YoungMiBot(config=config, ai_core=ai_core, intents=intents)

    # Initialize the Heartbeat
    heartbeat = Heartbeat(config=config, bot=bot, ai_core=ai_core)

    # We need to wrap the bot's startup and the heartbeat's start in an async context
    async def start_bot_and_heartbeat():
        # Using asyncio.gather to run both concurrently
        await asyncio.gather(
            bot.start(config.get("discord_bot_token")),
            heartbeat.start()
        )

    try:
        # Using a new async main function to run the bot
        asyncio.run(start_bot_and_heartbeat())
    except KeyboardInterrupt:
        logging.info("Shutdown signal received. Closing bot...")
    except Exception as e:
        logging.critical(f"A critical error occurred while running the bot: {e}")
    finally:
        # This part will run upon bot shutdown (e.g., Ctrl+C)
        async def cleanup():
            if heartbeat and heartbeat._task:
                logging.info("Stopping heartbeat...")
                await heartbeat.stop()

            if not bot.is_closed():
                logging.info("Closing Discord bot connection...")
                await bot.close()

            # Close API sessions
            sessions_to_close = [
                (ai_core.session, "AI Core"),
                (ai_core.image_generator.session, "Image Generator"),
                (ai_core.tts_generator.session, "TTS Generator")
            ]
            for session, name in sessions_to_close:
                if session and not session.closed:
                    logging.info(f"Shutting down {name} session...")
                    await session.close()
                    logging.info(f"{name} session closed.")

        logging.info("Starting cleanup...")
        try:
            # Find the running event loop to run cleanup
            loop = asyncio.get_running_loop()
            loop.run_until_complete(cleanup())
        except RuntimeError: # No running loop
            asyncio.run(cleanup())
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
        logging.info("Cleanup complete. Goodbye.")

if __name__ == "__main__":
    import os
    # Ensure the working directory is the project root
    if os.path.basename(os.getcwd()) == 'src':
        os.chdir('..')

    main()