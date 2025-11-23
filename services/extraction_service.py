# # import spacy

# # nlp = spacy.load("en_core_web_sm")

# # def extract_details(text):
# #     doc = nlp(text)

# #     details = {
# #         "productName": None,
# #         "brand": None,
# #         "color": None,
# #         "price": None,
# #     }

# #     for ent in doc.ents:
# #         if ent.label_ == "PRODUCT":
# #             details["productName"] = ent.text
# #         elif ent.label_ == "ORG":
# #             details["brand"] = ent.text
# #         elif ent.label_ == "MONEY":
# #             details["price"] = ent.text

# #     colors = ["red", "blue", "black", "white", "green", "yellow", "pink"]
# #     for c in colors:
# #         if c in text.lower():
# #             details["color"] = c
# #             break

# #     return details

# import spacy
# import re

# _nlp = None

# # Define multilingual keywords for better accuracy
# KEYWORDS = {
#     "colors": {
#         "green": ["green", "pacha"],
#         "red": ["red", "errupu"],
#         "blue": ["blue", "neelam"],
#         "black": ["black", "nalla"],
#         "white": ["white", "thella"]
#     },
#     "materials": {
#         "cotton": ["cotton", "patti"],
#         "silk": ["silk", "pattu"],
#     },
#     "products": {
#         "saree": ["saree", "cheera"],
#         "shirt": ["shirt", "chokka"]
#     }
# }

# def load_extraction_model():
#     """Loads the multilingual spaCy model."""
#     global _nlp
#     if _nlp is None:
#         # Use the multilingual model
#         model_name = "xx_ent_wiki_sm"
#         print(f"Loading spaCy model ({model_name})...")
#         try:
#             _nlp = spacy.load(model_name)
#             print("✅ spaCy model loaded.")
#         except IOError:
#             print(f"Error: spaCy model '{model_name}' not found.")
#             print(f"Please run: python -m spacy download {model_name}")
#             _nlp = None
#     return _nlp

# def extract_attributes(text):
#     """
#     Extracts attributes using a mix of smart regex and keyword matching.
#     """
#     nlp = load_extraction_model()
#     text_lower = text.lower()
    
#     attributes = {
#         "product_name": None,
#         "price": None,
#         "color": None,
#         "material": None
#     }

#     # 1. Extract Price (Robust Regex)
#     price_match = re.search(r'(\d+)\s*(rs|rupees|rupaya|/-)?', text_lower, re.IGNORECASE)
#     if price_match:
#         attributes["price"] = int(price_match.group(1))

#     # 2. Extract Keywords (Smarter loop)
#     for category, keyword_map in KEYWORDS.items():
#         for standard_name, synonyms in keyword_map.items():
#             for synonym in synonyms:
#                 if synonym in text_lower:
#                     if category == "colors":
#                         attributes["color"] = standard_name
#                     elif category == "materials":
#                         attributes["material"] = standard_name
#                     elif category == "products":
#                         attributes["product_name"] = standard_name
#                     break 
#             if attributes.get(category):
#                 break

#     # 3. Fallback Product Name (if no product keyword was found)
#     if attributes["product_name"] is None and nlp:
#         doc = nlp(text_lower)
#         for token in doc:
#             if token.pos_ == "NOUN":
#                 attributes["product_name"] = token.text
#                 break # Use the first noun

#     print(f"Extracted Attributes: {attributes}")
#     return attributes


import spacy
import re

_nlp = None

# ==============================================================================
# 
# COMPREHENSIVE E-COMMERCE KEYWORDS DICTIONARY
# 
# ==============================================================================
KEYWORDS = {
    # --- Primary Product Type (Broad) ---
    "products": {
        "saree": ["saree", "sari", "cheera"],
        "shirt": ["shirt", "shার্ট", "chokka"],
        "t-shirt": ["t-shirt", "tee", "tshirt"],
        "jeans": ["jeans", "jean"],
        "pants": ["pants", "pant", "trousers", "trouser", "pyjama"],
        "kurta": ["kurta", "kurti"],
        "dress": ["dress", "gown", "frock"],
        "jacket": ["jacket", "coat", "blazer"],
        "shoes": ["shoes", "shoe", "joote", "jootha", "sneakers", "boots", "heels", "sandals"],
        "pot": ["pot", "pots", "kunda", "patra", "vase", "planter"],
        "phone": ["phone", "mobile", "smartphone", "iphone"],
        "laptop": ["laptop", "computer", "macbook"],
        "headphones": ["headphones", "earbuds", "earphones", "airpods"],
        "tv": ["tv", "television", "smart tv"],
        "book": ["book", "kitab", "pustak", "novel"],
        "watch": ["watch", "ghadi", "smartwatch"],
        "bag": ["bag", "backpack", "handbag", "purse", "luggage", "suitcase"],
        "chair": ["chair", "kurchi", "stool"],
        "table": ["table", "desk", "balla"],
        "sofa": ["sofa", "couch"],
        "bed": ["bed", "cot"],
        "toy": ["toy", "gudiya", "khilona"],
        "necklace": ["necklace", "haar"],
        "earrings": ["earrings", "jhumka"],
        "ring": ["ring", "anguthi"],
        "bracelet": ["bracelet", "kangan"],
        "refrigerator": ["refrigerator", "fridge"],
        "fan": ["fan", "ceiling fan", "table fan"],
        "light": ["light", "bulb", "lamp"],
        "pan": ["pan", "frying pan", "cookware"],
        "bottle": ["bottle", "water bottle"],
    },
    
    # --- Target Audience ---
    "audience": {
        "men": ["men", "men's", "man", "purush", "aadmi"],
        "women": ["women", "women's", "woman", "mahila", "aurat"],
        "kids": ["kids", "kid", "children", "bachche"],
        "baby": ["baby", "infant", "shishu"],
        "unisex": ["unisex"],
    },

    # --- Colors ---
    "colors": {
        "green": ["green", "pacha", "hara"],
        "red": ["red", "errupu", "laal", "maroon"],
        "blue": ["blue", "neelam", "neela", "navy"],
        "black": ["black", "nalla", "kala", "charcoal"],
        "white": ["white", "thella", "safed", "ivory", "off-white"],
        "brown": ["brown", "godhuma", "bhura", "beige", "tan"],
        "yellow": ["yellow", "peela", "pasupu"],
        "orange": ["orange", "naarinja"],
        "pink": ["pink", "gulabi"],
        "purple": ["purple", "bengi", "violet", "lavender"],
        "grey": ["grey", "gray"],
        "silver": ["silver"],
        "gold": ["gold", "golden"],
        "multicolor": ["multicolor", "multi-color", "multi color"],
        "cream": ["cream"],
    },

    # --- Materials ---
    "materials": {
        "cotton": ["cotton", "patti", "sooti"],
        "silk": ["silk", "pattu", "resham"],
        "clay": ["clay", "matti", "ceramic", "porcelain"],
        "leather": ["leather", "chamada", "faux leather", "vegan leather"],
        "wool": ["wool", "woolen", "ooni"],
        "wood": ["wood", "wooden", "lakdi", "bamboo"],
        "plastic": ["plastic", "polycarbonate", "pvc"],
        "metal": ["metal", "iron", "steel", "aluminum", "brass", "copper"],
        "glass": ["glass"],
        "denim": ["denim"],
        "polyester": ["polyester"],
        "nylon": ["nylon"],
        "georgette": ["georgette"],
        "chiffon": ["chiffon"],
        "rayon": ["rayon"],
        "linen": ["linen"],
    },
    
    # --- Sizes ---
    "sizes": {
        "small": ["small", "s", "chota", "chinna"],
        "medium": ["medium", "m"],
        "large": ["large", "l", "bada", "pedda"],
        "xl": ["xl", "extra large"],
        "xxl": ["xxl"],
        "free size": ["free size", "one size"],
    },

    # --- Common Qualities / Descriptors ---
    "qualities": {
        "new": ["new", "kotha", "naya"],
        "old": ["old", "paatha", "purana", "used", "second-hand"],
        "handmade": ["handmade", "hand-made", "handcrafted"],
        "organic": ["organic"],
        "vintage": ["vintage", "antique"],
        "waterproof": ["waterproof", "water-proof"],
        "wireless": ["wireless", "bluetooth"],
        "4k": ["4k"],
        "hd": ["hd", "full hd"],
        "smart": ["smart"], # e.g., smart watch, smart tv
        "printed": ["printed", "print"],
        "embroidered": ["embroidered"],
        "solid": ["solid", "plain"],
        "striped": ["striped"],
        "checked": ["checked", "checkered"],
    }
}
# ==============================================================================


def load_extraction_model():
    """Loads the multilingual spaCy model."""
    global _nlp
    if _nlp is None:
        model_name = "xx_ent_wiki_sm"
        print(f"Loading spaCy model ({model_name})...")
        try:
            _nlp = spacy.load(model_name)
            print("✅ spaCy model loaded.")
        except IOError:
            print(f"Error: spaCy model '{model_name}' not found.")
            print(f"Please run: python -m spacy download {model_name}")
            _nlp = None
    return _nlp


def extract_attributes(text):
    """
    Extracts attributes using a mix of smart regex and keyword matching.
    This version supports multiple values and smarter product name generation.
    """
    nlp = load_extraction_model()
    text_lower = text.lower()
    
    attributes = {
        "product_name": None,
        "price": None,
        "audience": [],
        "colors": [],
        "materials": [],
        "sizes": [],
        "qualities": [],
    }

    # 1. Extract Price (Robust Regex)
    price_match = re.search(r'(\d+)\s*(rs|rupees|rupaya|/-)?', text_lower, re.IGNORECASE)
    if price_match:
        attributes["price"] = int(price_match.group(1))

    # 2. Extract Keywords (Smarter loop that appends to lists)
    
    # First, find the main product
    main_product = None
    for standard_name, synonyms in KEYWORDS["products"].items():
        for synonym in synonyms:
            if synonym in text_lower:
                main_product = standard_name
                break
        if main_product:
            break

    # Now, find all other attributes
    for category, keyword_map in KEYWORDS.items():
        if category == "products":
            continue # Already handled

        attr_key = category # e.g., "colors", "materials", "sizes"
        
        for standard_name, synonyms in keyword_map.items():
            for synonym in synonyms:
                if synonym in text_lower:
                    if standard_name not in attributes[attr_key]:
                        attributes[attr_key].append(standard_name)
                    break 

    # 3. Build a "Smarter" Product Name
    # Combines audience, qualities, materials, and product
    # e.g., "men" + "printed" + "cotton" + "shirt" -> "men printed cotton shirt"
    
    smart_name_parts = []
    
    # Prepend audience
    if attributes["audience"]:
        smart_name_parts.append(attributes["audience"][0])
        
    # Prepend qualities
    if attributes["qualities"]:
        smart_name_parts.extend(attributes["qualities"])
        
    # Prepend materials
    if attributes["materials"]:
        smart_name_parts.append(attributes["materials"][0])
        
    # Add main product
    if main_product:
        smart_name_parts.append(main_product)

    if smart_name_parts:
        attributes["product_name"] = " ".join(smart_name_parts)
    
    # 4. Fallback Product Name (if no product keyword was found)
    if attributes["product_name"] is None and nlp:
        doc = nlp(text_lower)
        for token in doc:
            # Find the first main noun
            if token.pos_ == "NOUN" and not token.is_stop:
                attributes["product_name"] = token.text
                break 

    print(f"Extracted Attributes: {attributes}")
    return attributes