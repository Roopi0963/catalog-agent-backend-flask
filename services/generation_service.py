# # from transformers import pipeline

# # generator = pipeline("text-generation", model="gpt2")

# # def generate_description(data):
# #     product = data.get("productName", "product")
# #     brand = data.get("brand", "brand")
# #     color = data.get("color", "color")
# #     price = data.get("price", "price")

# #     prompt = (
# #         f"Write a short professional product description for a "
# #         f"{color} {product} from {brand} priced at {price}. "
# #         f"Keep it under 60 words."
# #     )

# #     output = generator(prompt, max_length=60, num_return_sequences=1)[0]["generated_text"]

# #     return output


# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_description(data):
#     product = data.get("productName", "product")
#     color = data.get("color", "unknown")
#     brand = data.get("brand", "unknown")
#     price = data.get("price", "not specified")

#     prompt = f"""
# Generate a short product description in bullet points only.
# Keep exactly 5–7 bullet points.
# Each bullet must be a crisp, simple sentence.
# NO PARAGRAPHS.

# Product: {product}
# Brand: {brand}
# Color: {color}
# Price: {price}
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response.choices[0].message["content"]

#     except Exception as e:
#         return f"Error generating description: {str(e)}"

# from transformers import T5ForConditionalGeneration, T5Tokenizer

# _tokenizer = None
# _model = None

# def load_generation_model():
#     """Loads the FLAN-T5 model and tokenizer into memory."""
#     global _tokenizer, _model
#     if _tokenizer is None or _model is None:
        
#         # Use Google's instruction-tuned model
#         model_name = "google/flan-t5-base"
        
#         print(f"Loading T5 model ({model_name})...")
#         _tokenizer = T5Tokenizer.from_pretrained(model_name)
#         _model = T5ForConditionalGeneration.from_pretrained(model_name)
#         print(f"✅ T5 model ({model_name}) loaded.")
#     return _tokenizer, _model

# def generate_description(attributes):
#     """
#     Generates a product description using FLAN-T5.
#     """
#     tokenizer, model = load_generation_model()
    
#     prompt = f"generate a short, attractive e-commerce product description for a product with these details: {str(attributes)}"
    
#     print(f"Generating description for prompt: {prompt}")

#     inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
#     outputs = model.generate(
#         inputs, 
#         max_length=150, 
#         num_beams=4, 
#         early_stopping=True
#     )
#     description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     print(f"Generated Description: {description}")
#     return description

import requests
import json

# 1. Set the model to Qwen 2.5
MODEL_NAME = "qwen2.5" 
OLLAMA_URL = "http://localhost:11434/api/generate"

# 2. Qwen's Native "ChatML" Prompt Template
# This format (<|im_start|>) is what Qwen was trained on. 
# Using it makes the model much smarter and more obedient.
PROMPT_TEMPLATE = """<|im_start|>system
You are an expert e-commerce cataloging assistant. 
Your task is to extract product attributes from the user's text and output them in strict JSON format.
Do not include any conversational text (like "Here is the JSON"). Output ONLY the JSON object.
<|im_end|>
<|im_start|>user
Analyze this vendor's voice transcript: "{text}"

Extract the data into this exact JSON structure:
{{
  "extracted_attributes": {{
    "product_name": "string (e.g., 'Cotton Saree')",
    "price": number or null,
    "audience": ["men", "women", "kids", "unisex"],
    "colors": ["string"],
    "materials": ["string"],
    "qualities": ["string (e.g., 'handmade', 'new')"]
  }},
  "generated_content": {{
    "product_description_en": "A professional, attractive e-commerce product description in English (max 50 words)."
  }}
}}
<|im_end|>
<|im_start|>assistant
"""

def get_product_data(text):
    """
    Calls the local Ollama model (Qwen 2.5) to get product data.
    """
    # Sanitize quotes to prevent JSON errors
    clean_text = text.replace('"', "'").replace('\n', ' ')
    
    # Inject the text into the template
    prompt = PROMPT_TEMPLATE.format(text=clean_text)
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json", # Critical: Forces Qwen to output valid JSON
        "temperature": 0.2 # Keep it low (0.2) for accuracy. High temp = creative/hallucinations.
    }
    
    print(f"Sending request to Ollama ({MODEL_NAME})...")

    try:
        # Qwen is usually faster, so 60s timeout is plenty
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        response_data = response.json()
        product_data_string = response_data.get('response')
        
        if not product_data_string:
            raise Exception("Ollama returned an empty response.")
        
        # Parse the JSON string from the model
        product_data_json = json.loads(product_data_string)
        
        print("Successfully received data from Qwen 2.5.")
        return product_data_json

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return {
            "extracted_attributes": {"error": f"Connection error: {str(e)}"},
            "generated_content": {"product_description_en": "Error: AI Service Unavailable"}
        }
    except json.JSONDecodeError as e:
        print(f"Error: Qwen returned invalid JSON. Raw output: {product_data_string}")
        return {
            "extracted_attributes": {"error": "AI returned bad data"},
            "generated_content": {"product_description_en": "Error parsing AI data."}
        }
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return {
            "extracted_attributes": {"error": str(e)},
            "generated_content": {"product_description_en": "An unknown error occurred."}
        }