#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start (important!)
echo "Waiting for Ollama..."
sleep 5

# Pull the model (downloads it inside the cloud container)
echo "Pulling Qwen Model..."
ollama pull qwen2.5

# Start Flask App
echo "Starting Flask..."
python app.py