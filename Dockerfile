# FROM python:3.9-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     ffmpeg \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Install Ollama
# RUN curl -fsSL https://ollama.com/install.sh | sh

# # Set working directory
# WORKDIR /app

# # Copy requirements and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all application files
# COPY . .

# # Grant execution permissions to start script
# RUN chmod +x start.sh

# # Create a writable directory for uploads (Crucial for Hugging Face)
# RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# # Expose the required port
# EXPOSE 7860

# # Run the start script
# CMD ["./start.sh"]



FROM python:3.9-slim

# Install system dependencies
# ADDED: build-essential and python3-dev to fix the 'gcc' missing error
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Grant execution permissions to start script
RUN chmod +x start.sh

# Create a writable directory for uploads (Crucial for Hugging Face)
RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# Expose the required port
EXPOSE 7860

# Run the start script
CMD ["./start.sh"]