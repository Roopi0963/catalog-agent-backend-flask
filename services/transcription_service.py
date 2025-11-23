# import librosa
# from transformers import pipeline

# # Load free Whisper
# asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# def transcribe_audio(file_path):
#     audio, sr = librosa.load(file_path, sr=16000)
#     result = asr(audio)["text"]
#     return result

# import whisper
# import os

# _model = None

# def load_transcription_model():
#     """Loads the Whisper model into memory."""
#     global _model
#     if _model is None:
#         print("Loading Whisper model (medium)... This will take time and memory.")
#         # "medium" model for high accuracy
#         _model = whisper.load_model("medium")
#         print("✅ Whisper model (medium) loaded.")
#     return _model

# def transcribe_audio(audio_path):
#     """
#     Transcribes audio using Whisper.
#     Returns: A dictionary with 'text' and 'language'.
#     """
#     model = load_transcription_model()
    
#     print(f"Transcribing {audio_path}...")
#     # fp16=False is safer for CPU-only execution
#     result = model.transcribe(audio_path, fp16=False) 
    
#     print(f"Transcription: {result['text']}")
#     return {
#         "text": result["text"],
#         "language": result["language"]
#     }

# # In services/transcription_service.py

# # --- NEW: Accept the language_code parameter ---
# def transcribe_audio(audio_path, language_code=None):
#     """
#     Transcribes audio using Whisper.
#     Returns: A dictionary with 'text' and 'language'.
#     """
#     model = load_transcription_model()
    
#     print(f"Transcribing {audio_path} (Forced language: {language_code})...")
    
#     # --- NEW: Pass the language code to Whisper's transcribe function ---
#     result = model.transcribe(audio_path, language=language_code, fp16=False) 
    
#     print(f"Transcription: {result['text']}")
#     return {
#         "text": result["text"],
#         "language": result["language"] # This will now be 'en'
#     }


import whisper
import os

_model = None

def load_transcription_model():
    global _model
    if _model is None:
        print("Loading Whisper model (medium)...")
        _model = whisper.load_model("medium") # Or large-v3 for best results
        print("✅ Whisper model loaded.")
    return _model

def transcribe_audio(audio_path, language_code=None):
    model = load_transcription_model()
    
    print(f"Transcribing {audio_path}...")

    # --- THE MAGIC CHANGE IS HERE ---
    # task="translate" tells Whisper: "Whatever language you hear, write it down in English."
    result = model.transcribe(
        audio_path, 
        language=language_code, 
        fp16=False,
        task="translate"  # <--- ADD THIS LINE
    ) 
    
    print(f"Translated Transcription: {result['text']}")
    return {
        "text": result["text"],
        "language": result["language"] # It still tells you what the original language was!
    }