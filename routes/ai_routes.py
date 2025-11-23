# from flask import Blueprint, request, jsonify
# from services.transcription import transcribe_audio
# from services.extraction import extract_details
# from services.generation import generate_description

# ai_routes = Blueprint("ai_routes", __name__, url_prefix="/api")

# # ----------------------------
# # 1. TRANSCRIBE AUDIO
# # ----------------------------
# @ai_routes.route("/transcribe", methods=["POST"])
# def transcribe():
#     if "audio" not in request.files:
#         return jsonify({"error": "No audio file provided"}), 400

#     audio_file = request.files["audio"]
#     filepath = "temp_audio.wav"
#     audio_file.save(filepath)

#     text = transcribe_audio(filepath)
#     return jsonify({"transcription": text})


# # ----------------------------
# # 2. EXTRACT DETAILS
# # ----------------------------
# @ai_routes.route("/extract-details", methods=["POST"])
# def extract_info():
#     data = request.get_json()
#     text = data.get("text", "")
#     details = extract_details(text)
#     return jsonify(details)


# # ----------------------------
# # 3. GENERATE DESCRIPTION
# # ----------------------------
# @ai_routes.route("/generate-description", methods=["POST"])
# def gen_description():
#     data = request.get_json()
#     description = generate_description(data)
#     return jsonify({"description": description})
