# from flask import Flask
# from flask_cors import CORS
# from routes.ai_routes import ai_routes

# app = Flask(__name__)
# CORS(app)

# app.register_blueprint(ai_routes)

# if __name__ == "__main__":
#     app.run(debug=True)


# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from services import transcription_service, extraction_service, generation_service

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # --- 1. Pre-load All Models on Startup ---
# # This is crucial for performance.
# with app.app_context():
#     print("Pre-loading all AI models...")
#     transcription_service.load_transcription_model()
#     extraction_service.load_extraction_model()
#     generation_service.load_generation_model()
#     print("--- All models loaded. Ready for requests! ---")


# # --- 2. The Main API Endpoint ---
# # @app.route('/api/process-voice', methods=['POST'])
# # def process_voice_to_catalog():
# #     """
# #     Main API endpoint: Receives audio, returns full JSON.
# #     """
# #     if 'audio' not in request.files:
# #         return jsonify({"error": "No audio file provided"}), 400

# #     audio_file = request.files['audio']
    
# #     # Use a secure, unique filename in a real app
# #     temp_audio_path = "temp_audio_file.wav" 
# #     audio_file.save(temp_audio_path)

# #     try:
# #         # Step 1: Speech-to-Text
# #         transcription_data = transcription_service.transcribe_audio(temp_audio_path)
# #         original_text = transcription_data["text"]
# #         language = transcription_data["language"]
# # In app.py

# @app.route('/api/process-voice', methods=['POST'])
# def process_voice_to_catalog():
#     """
#     Main API endpoint: Receives audio, returns full JSON.
#     """
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files['audio']
    
#     # --- NEW: Get the language code from the form ---
#     # Default to None to let Whisper auto-detect if not provided
#     language_code = request.form.get('language', None) 
#     print(f"Received request with language: {language_code}")
    
#     temp_audio_path = "temp_audio_file.wav" 
#     audio_file.save(temp_audio_path)

#     try:
#         # --- NEW: Pass the language code to the service ---
#         transcription_data = transcription_service.transcribe_audio(temp_audio_path, language_code)
        
#         original_text = transcription_data["text"]
#         language = transcription_data["language"]
        
#         # ... rest of the function ...
#         # Step 2: Attribute Extraction
#         attributes = extraction_service.extract_attributes(original_text)

#         # Step 3: Description Generation
#         ai_description = generation_service.generate_description(attributes)
        
#         # Clean up the temp file
#         os.remove(temp_audio_path)

#         # Return the full, structured JSON
#         return jsonify({
#             "success": True,
#             "language_detected": language,
#             "original_transcription": original_text,
#             "extracted_attributes": attributes,
#             "generated_content": {
#                 "product_description_en": ai_description,
#                 "suggested_tags": ["tag1", "tag2"] # Placeholder for tags
#             }
#         }), 200

#     except Exception as e:
#         # Clean up the temp file even if an error occurs
#         if os.path.exists(temp_audio_path):
#             os.remove(temp_audio_path)
#         print(f"An error occurred: {e}")
#         return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

# @app.route('/')
# def health_check():
#     return jsonify({"status": "Flask AI Service is running!"})

# if __name__ == '__main__':
#     # Use port 5001 as defined in your docker-compose
#     app.run(host='0.0.0.0', port=5001)

# import os
# import uuid  # We need this for unique filenames
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from services import transcription_service, extraction_service, generation_service

# app = Flask(__name__)
# CORS(app)

# # Load models on startup
# with app.app_context():
#     print("Loading AI Models...")
#     transcription_service.load_transcription_model()
#     extraction_service.load_extraction_model()
#     generation_service.load_generation_model()
#     print("Models Loaded.")

# @app.route('/api/process-voice', methods=['POST'])
# def process_voice_to_catalog():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files['audio']
    
#     # 1. Save file uniquely
#     filename = f"{uuid.uuid4()}.wav"
#     temp_path = os.path.join("temp_uploads", filename)
#     os.makedirs("temp_uploads", exist_ok=True)
#     audio_file.save(temp_path)

#     try:
#         # 2. Process
#         transcription = transcription_service.transcribe_audio(temp_path)
#         text = transcription["text"]
        
#         attributes = extraction_service.extract_attributes(text)
#         description = generation_service.generate_description(attributes)

#         # 3. Return JSON in the structure React expects
#         return jsonify({
#             "success": True,
#             "data": {
#                 "productName": attributes.get("product_name") or "New Product",
#                 "brand": "Generic",
#                 "price": attributes.get("price") or 0,
#                 "color": attributes.get("colors", [""])[0] if attributes.get("colors") else "",
#                 "description": description,
#                 "tags": ", ".join(attributes.get("audience", []) + attributes.get("materials", []))
#             }
#         }), 200

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# --- UPDATED IMPORTS ---
from services import transcription_service, generation_service

app = Flask(__name__)
CORS(app)

# --- 1. Pre-load Models ---
with app.app_context():
    print("Pre-loading all AI models...")
    transcription_service.load_transcription_model()
    # We no longer load spaCy or T5! Ollama handles the rest.
    print("--- All models loaded. Ready for requests! ---")


# --- 2. The Main API Endpoint ---
@app.route('/api/process-voice', methods=['POST'])
def process_voice_to_catalog():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    language_code = request.form.get('language', None)
    temp_audio_path = "temp_audio_file.wav" 
    audio_file.save(temp_audio_path)

    try:
        # --- Step 1: Speech-to-Text (Same as before) ---
        transcription_data = transcription_service.transcribe_audio(temp_audio_path, language_code)
        original_text = transcription_data["text"]
        language = transcription_data["language"]

        # --- Step 2: Get ALL data from Generative AI (Replaces 2 steps) ---
        # This one function does both extraction AND generation
        product_data = generation_service.get_product_data(original_text)
        
        os.remove(temp_audio_path)

        # --- Step 3: Return the combined JSON ---
        return jsonify({
            "success": True,
            "language_detected": language,
            "original_transcription": original_text,
            "extracted_attributes": product_data.get("extracted_attributes"),
            "generated_content": product_data.get("generated_content")
        }), 200

    except Exception as e:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        print(f"An error occurred in app.py: {e}")
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "Flask AI Service is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)