# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# # — Hard-coded Gemini API key —
# genai.configure(api_key="AIzaSyBiaof7N5FhqttxuXUFXspLa-B7dBPh7l0")

# # Load the Gemini model
# model = genai.GenerativeModel("gemini-pro")

# @app.route("/analyze", methods=["POST"])
# def analyze_product():
#     data = request.get_json()
#     product_text = data.get("productText", "")
#     if not product_text:
#         return jsonify({"error": "No product text provided"}), 400

#     prompt = f"""
# You are a sustainability expert. Analyze the environmental impact of this product description.
# Respond with:
# 1. Eco-Friendliness Score (1–10)
# 2. Main environmental concerns
# 3. Sustainable alternatives (if any)

# Product Description:
# {product_text}
# """
#     try:
#         response = model.generate_content(prompt)
#         return jsonify({"result": response.text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# — Hard-coded Gemini API key —
genai.configure(api_key="AIzaSyBiaof7N5FhqttxuXUFXspLa-B7dBPh7l0")  # Ensure your API key is here

# Load the Gemini model with the suggested name
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/analyze", methods=["POST"])
def analyze_product():
    data = request.get_json()
    product_text = data.get("productText", "")
    if not product_text:
        return jsonify({"error": "No product text provided"}), 400

    prompt = f"""
You are a sustainability expert. Analyze the environmental impact of this product description.
Respond with:
1. Eco-Friendliness Score (1–10)
2. Main environmental concerns
3. Sustainable alternatives (if any)

Product Description:
{product_text}
"""
    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list_models", methods=["GET"])
def list_models():
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        return jsonify({"available_models": model_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)