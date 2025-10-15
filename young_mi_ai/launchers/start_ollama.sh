#!/bin/bash
# --- ONE-TIME SETUP ---
# On macOS and Linux, Ollama is typically run as a system service.
# This script simply ensures it's running. If you run it from a specific
# location, you can replace the command below.

echo "Starting Ollama..."
# The 'ollama serve' command will start the server if it's not already running.
# We run it in the background (&) so the script can continue.
ollama serve > /dev/null 2>&1 &

echo "Ollama is starting in the background."
sleep 3