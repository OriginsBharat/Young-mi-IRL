#!/bin/bash
# --- ONE-TIME SETUP ---
# 1. Find your ComfyUI installation directory.
# 2. Replace the placeholder path below with the full path to that directory.
#    - Example: COMFYUI_DIR="/home/user/ComfyUI"

echo "Starting ComfyUI..."

# --- EDIT THE PATH BELOW ---
COMFYUI_DIR="/path/to/your/ComfyUI"
# --- END OF SETUP ---

if [ -d "$COMFYUI_DIR" ]; then
  cd "$COMFYUI_DIR"
  # Run ComfyUI in the background
  python3 main.py > /dev/null 2>&1 &
  echo "ComfyUI is starting in the background."
else
  echo "Error: ComfyUI directory not found at $COMFYUI_DIR"
  echo "Please edit this script to set the correct path."
fi

sleep 3