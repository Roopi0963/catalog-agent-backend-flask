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


# 1. CHANGE: Upgrade to Python 3.10. 
# 3.9 is older and sometimes misses pre-built wheels for newer libraries like Spacy.
FROM python:3.10-slim

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

# Upgrade pip
RUN pip install --upgrade pip

# 2. OPTIMIZATION: Install CPU Torch (Keep this, it worked great!)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. FIX: Install Spacy separately first to ensure we get a binary
# This prevents the 28-minute compile time.
RUN pip install --no-cache-dir spacy==3.8.2 --only-binary=:all:

# 4. Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Grant execution permissions
RUN chmod +x start.sh

# Create uploads directory
RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# Expose port
EXPOSE 7860

CMD ["./start.sh"]