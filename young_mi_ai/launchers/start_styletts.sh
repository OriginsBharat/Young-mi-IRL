#!/bin/bash
# --- ONE-TIME SETUP ---
# 1. Follow the instructions in the main README to install StyleTTS 2.
# 2. Find the 'StyleTTS2-Sillytavern-api' folder you created.
# 3. Replace the placeholder path below with the full path to that directory.
#    - Example: STYLETTS_DIR="/home/user/StyleTTS2-Sillytavern-api"

echo "Starting StyleTTS 2 API Server..."

# --- EDIT THE PATH BELOW ---
STYLETTS_DIR="/path/to/your/StyleTTS2-Sillytavern-api"
# --- END OF SETUP ---

if [ -d "$STYLETTS_DIR" ]; then
  cd "$STYLETTS_DIR"

  # Activate virtual environment if it exists
  if [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
  fi

  echo "Launching StyleTTS 2 API..."
  python3 api.py > /dev/null 2>&1 &
  echo "StyleTTS 2 API is starting in the background."
else
  echo "Error: StyleTTS 2 directory not found at $STYLETTS_DIR"
  echo "Please edit this script to set the correct path."
fi

sleep 3