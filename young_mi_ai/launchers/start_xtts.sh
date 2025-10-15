#!/bin/bash
# --- ONE-TIME SETUP ---
# 1. Find your XTTS web UI installation directory (e.g., xtts-webui).
# 2. Replace the placeholder path below with the full path to that directory.
#    - Example: XTTS_DIR="/home/user/xtts-webui"

echo "Starting XTTSv2 Server..."

# --- EDIT THE PATH BELOW ---
XTTS_DIR="/path/to/your/xtts-webui"
# --- END OF SETUP ---

if [ -d "$XTTS_DIR" ]; then
  cd "$XTTS_DIR"
  # This assumes a 'start.sh' or similar script. Adjust if necessary.
  # Run XTTS in the background
  ./start.sh > /dev/null 2>&1 &
  echo "XTTS is starting in the background."
else
  echo "Error: XTTS directory not found at $XTTS_DIR"
  echo "Please edit this script to set the correct path."
fi

sleep 3