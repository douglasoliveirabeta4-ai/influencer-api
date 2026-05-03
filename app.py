from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, base64, os

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V6.0_B1_noVAE"

@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.json
    prompt = data.get("prompt", "")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"width": 512, "height": 768}}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    if response.status_code != 200:
        return jsonify({"erro": response.text}), 500
    img_b64 = base64.b64encode(response.content).decode("utf-8")
    return jsonify({"imagem": f"data:image/jpeg;base64,{img_b64}"})

@app.route("/")
def index():
    return "API rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
