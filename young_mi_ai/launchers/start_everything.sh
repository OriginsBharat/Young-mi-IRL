#!/bin/bash
# This script will start all necessary components for the Kim Young-mi AI.
# Make sure you have configured the individual .sh files in this folder first.

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "================================="
echo "  Starting All Services..."
echo "================================="
echo

echo "[1/4] Starting Ollama..."
bash "$DIR/start_ollama.sh"
sleep 5

echo "[2/4] Starting ComfyUI..."
bash "$DIR/start_comfyui.sh"
sleep 10

echo "[3/4] Starting StyleTTS 2 Server..."
bash "$DIR/start_styletts.sh"
sleep 10

echo "[4/4] Starting Kim Young-mi Bot..."
echo
# Go to the parent directory to run the bot
cd "$DIR/.."
python3 src/main.py

echo
echo "================================="
echo "  All services are running."
echo "================================="