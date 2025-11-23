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



# FROM python:3.9-slim

# # Install system dependencies
# # ADDED: build-essential and python3-dev to fix the 'gcc' missing error
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
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

# Copy requirements
COPY requirements.txt .

# --- OPTIMIZATION START ---
# 1. Upgrade pip so it finds pre-built wheels (Fixes Spacy compilation time)
RUN pip install --upgrade pip

# 2. Install CPU-only version of Torch FIRST (Saves ~2GB of download and 5-10 mins)
# If you actually HAVE a GPU in production, remove the "--index-url" part.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt
# --- OPTIMIZATION END ---

# Copy all application files
COPY . .

# Grant execution permissions
RUN chmod +x start.sh

# Create uploads directory
RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# Expose port
EXPOSE 7860

CMD ["./start.sh"]