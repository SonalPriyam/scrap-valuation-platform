import os
import random
import pandas as pd

IMAGE_DIR = "dataset"

REAL_MARKET_DESCRIPTIONS = {
    "metal": [
        "Mixed industrial metal scraps, beverage cans, and broken sheet panels.",
        "Clean scrap metal collection leftover from mechanical workshop sorting.",
        "Crushed metal containers and iron pieces accumulated from factory floor clearance."
    ],
    "plastic": [
        "Bulk crushed PET plastic bottles and high-density polyethylene containers.",
        "Industrial plastic crates and discarded packaging materials lot.",
        "Assorted clear plastic sheets and scrap fragments ready for shredding."
    ],
    "glass": [
        "Clear and colored glass bottle scrap from beverage disposal processing.",
        "Broken window pane glass shards and laboratory glassware waste pieces.",
        "Mixed cullet glass scraps sorted by weight for foundry recycling."
    ],
    "paper": [
        "Bundled old newspapers and clean white office paper scrap rows.",
        "Shredded confidential documents and high-grade printing paper waste bales.",
        "Mixed bulk paper scrap collected from corporate office recycle bins."
    ],
    "cardboard": [
        "Corrugated cardboard boxes flattened and bound for industrial pulping.",
        "Heavy-duty packaging cartons and shipping boxes scrap material.",
        "Discarded grocery cardboard scraps accumulated behind retail warehouse."
    ],
    "trash": [
        "Mixed municipal solid waste, floor sweeping debris, and non-recyclable items.",
        "Unsorted household waste fragments mixed with organic and fabric remnants.",
        "General reject stream waste from conveyor belt initial sorting phase."
    ]
}

COMMODITY_PRICES = {
    "metal": 55.0,
    "plastic": 22.0,
    "glass": 12.0,
    "paper": 14.0,
    "cardboard": 18.0,
    "trash": 2.0
}

QUALITY_MODIFIERS = [0.70, 1.0, 1.30]
QUALITY_LABELS = ["low", "moderate", "high"]

def bind_text_to_real_images():
    rows = []
    target_folders = ["trash", "plastic", "paper", "metal", "glass", "cardboard"]

    print("Scanning dataset directories...")

    for category in target_folders:
        folder_path = os.path.join(IMAGE_DIR, category)

        if not os.path.exists(folder_path):
            print(f"Directory missing: '{folder_path}'.")
            continue

        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if len(image_files) == 0:
            print(f"No image files found in '{category}/'.")
            continue

        print(f"Found {len(image_files)} images in [{category.upper()}]")

        for idx, img_name in enumerate(image_files):
            full_img_path = os.path.join(folder_path, img_name)

            text_pool = REAL_MARKET_DESCRIPTIONS[category]
            base_text = text_pool[idx % len(text_pool)]

            random.seed(idx)
            weight = round(random.uniform(10.0, 600.0), 1)

            final_text = f"[{weight} KG] {base_text}"

            q_idx = idx % 3
            quality_label = QUALITY_LABELS[q_idx]
            modifier = QUALITY_MODIFIERS[q_idx]

            base_rate = COMMODITY_PRICES[category]
            target_price = round(base_rate * weight * modifier, 2)

            rows.append({
                "text_description": final_text,
                "image_path": full_img_path,
                "true_material": category,
                "true_weight_kg": weight,
                "surface_purity_grade": quality_label,
                "target_valuation_inr": target_price
            })

    if rows:
        df = pd.DataFrame(rows)
        df.to_csv("dataset/final_multimodal_dataset.csv", index=False)

        print("\nDataset saved successfully.")
        print(f"Total rows generated: {len(df)}")
    else:
        print("Dataset generation failed. Verify folder paths.")

if __name__ == "__main__":
    bind_text_to_real_images()