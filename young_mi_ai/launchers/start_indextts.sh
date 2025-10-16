#!/bin/bash
# --- ONE-TIME SETUP ---
# 1. Follow the instructions in the main README to install IndexTTS One-Click.
# 2. Find the 'index-tts-OneClick' folder you created.
# 3. Replace the placeholder path below with the full path to that directory.
#    - Example: INDEXTTS_DIR="/home/user/index-tts-OneClick"

echo "Starting IndexTTS API Server..."

# --- EDIT THE PATH BELOW ---
INDEXTTS_DIR="/path/to/your/index-tts-OneClick"
# --- END OF SETUP ---

if [ -d "$INDEXTTS_DIR" ]; then
  cd "$INDEXTTS_DIR"

  echo "Launching IndexTTS API..."
  # This assumes a 'run-http.sh' or similar script exists for non-Windows.
  # If not, the user may need to adjust this command.
  if [ -f "./run-http.sh" ]; then
    bash ./run-http.sh > /dev/null 2>&1 &
  else
    echo "Warning: 'run-http.sh' not found. You may need to create one or run the server manually."
  fi
  echo "IndexTTS API is starting in the background."
else
  echo "Error: IndexTTS directory not found at $INDEXTTS_DIR"
  echo "Please edit this script to set the correct path."
fi

sleep 3