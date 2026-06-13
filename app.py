import os
import io
import re
import pickle
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI(title="Multimodal Scrap Valuation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

MODEL_DIR = "models"
CNN_MODEL_PATH = os.path.join(MODEL_DIR, "cnn_vision_model.keras")
REGRESSOR_PATH = os.path.join(MODEL_DIR, "valuation_regressor.pkl")

print("Loading models...")

try:
    cv_extractor = tf.keras.models.load_model(CNN_MODEL_PATH)

    with open(REGRESSOR_PATH, "rb") as f:
        artifacts = pickle.load(f)

    valuation_regressor = artifacts["regressor"]
    material_encoder = artifacts["material_encoder"]
    purity_encoder = artifacts["purity_encoder"]

    print("Models loaded successfully.")

except Exception as e:
    print(f"Initialization warning: {str(e)}")
    print("Ensure model files exist inside the models folder.")

def clean_and_parse_text(text: str):
    text_lower = text.lower()

    weight = 50.0

    weight_match = re.search(
        r'(\d+(?:\.\d+)?)\s*(?:kg|kilogram|kgs|kilos)',
        text_lower
    )

    if weight_match:
        weight = float(weight_match.group(1))

    detected_material = "trash"

    target_categories = [
        "trash",
        "plastic",
        "paper",
        "metal",
        "glass",
        "cardboard"
    ]

    for category in target_categories:
        if category in text_lower:
            detected_material = category
            break

    return detected_material, weight

@app.get("/", response_class=HTMLResponse)
def serve_frontend_dashboard():
    index_path = os.path.join("templates", "index.html")

    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()

    return "<h1>templates/index.html not found.</h1>"

@app.post("/api/v1/valuate")
async def execute_live_valuation(
    text_description: str = Form(...),
    image_file: UploadFile = File(...)
):
    try:
        material, weight = clean_and_parse_text(text_description)

        img_bytes = await image_file.read()

        img = (
            Image.open(io.BytesIO(img_bytes))
            .convert("RGB")
            .resize((224, 224))
        )

        img_array = tf.keras.preprocessing.image.img_to_array(img)

        img_tensor = np.expand_dims(img_array, axis=0) / 255.0

        visual_embeddings = cv_extractor.predict(img_tensor)

        try:
            encoded_material = material_encoder.transform([material])[0]

        except ValueError:
            encoded_material = material_encoder.transform(["trash"])[0]
            material = "trash"

        pixel_mean = np.mean(img_tensor)

        if pixel_mean < 0.4:
            inferred_purity = "low"
        elif pixel_mean > 0.7:
            inferred_purity = "high"
        else:
            inferred_purity = "moderate"

        encoded_purity = purity_encoder.transform([inferred_purity])[0]

        tabular_features = np.array([
            [encoded_material, weight, encoded_purity]
        ])

        unified_feature_vector = np.hstack(
            (tabular_features, visual_embeddings)
        )

        predicted_price = valuation_regressor.predict(
            unified_feature_vector
        )[0]

        price_lower = max(
            0.0,
            round(predicted_price * 0.9, 2)
        )

        price_upper = round(
            predicted_price * 1.1,
            2
        )

        return {
            "status": "success",
            "extracted_data": {
                "classified_material": material.upper(),
                "parsed_weight": f"{weight} KG",
                "condition_grade": inferred_purity.upper()
            },
            "valuation_output": {
                "base_currency": "INR (₹)",
                "midpoint_estimation": f"₹{predicted_price:,.2f}",
                "market_price_range": f"₹{price_lower:,} - ₹{price_upper:,}"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference breakdown error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )