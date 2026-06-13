## Done in Google Colab

# import os
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import RandomForestRegressor
# import pickle

# DATASET_PATH = "/content/drive/MyDrive/dataset/final_multimodal_dataset.csv"

# if not os.path.exists(DATASET_PATH):
#     raise FileNotFoundError(f"Missing {DATASET_PATH}")

# df = pd.read_csv(DATASET_PATH)

# df["image_path"] = (
#     "/content/drive/MyDrive/" +
#     df["image_path"].str.replace("\\", "/", regex=False)
# )

# print("Dataset loaded. Processing image features via Transfer Learning...")

# print(df["image_path"].head())
# print("First image exists:", os.path.exists(df["image_path"].iloc[0]))

# def load_and_preprocess_image(path):
#     img = tf.io.read_file(path)
#     img = tf.image.decode_image(
#         img,
#         channels=3,
#         expand_animations=False
#     )
#     img = tf.image.resize(img, [224, 224])
#     img = img / 255.0
#     return img

# image_paths = df["image_path"].values

# image_ds = (
#     tf.data.Dataset
#     .from_tensor_slices(image_paths)
#     .map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
#     .batch(32)
#     .prefetch(tf.data.AUTOTUNE)
# )

# base_model = tf.keras.applications.MobileNetV2(
#     input_shape=(224, 224, 3),
#     include_top=False,
#     weights="imagenet"
# )

# base_model.trainable = False

# image_feature_extractor = tf.keras.Sequential([
#     base_model,
#     tf.keras.layers.GlobalAveragePooling2D()
# ])

# print("Extracting visual embeddings from images...")

# visual_features = image_feature_extractor.predict(image_ds)

# material_encoder = LabelEncoder()
# encoded_materials = material_encoder.fit_transform(df["true_material"])

# purity_encoder = LabelEncoder()
# encoded_purity = purity_encoder.fit_transform(df["surface_purity_grade"])

# X_tabular = np.column_stack((
#     encoded_materials,
#     df["true_weight_kg"].values,
#     encoded_purity
# ))

# X_unified = np.hstack((X_tabular, visual_features))

# y = df["target_valuation_inr"].values

# X_train, X_test, y_train, y_test = train_test_split(
#     X_unified,
#     y,
#     test_size=0.2,
#     random_state=42
# )

# print(f"Training Ensemble Valuation Regressor on {X_train.shape[0]} samples...")

# regressor = RandomForestRegressor(
#     n_estimators=100,
#     random_state=42,
#     n_jobs=-1
# )

# regressor.fit(X_train, y_train)

# train_score = regressor.score(X_train, y_train)
# test_score = regressor.score(X_test, y_test)

# print(f"Training Accuracy: {train_score * 100:.2f}%")
# print(f"Test Accuracy: {test_score * 100:.2f}%")

# os.makedirs("models", exist_ok=True)

# image_feature_extractor.save("models/cnn_vision_model.keras")

# artifacts = {
#     "regressor": regressor,
#     "material_encoder": material_encoder,
#     "purity_encoder": purity_encoder
# }

# with open("models/valuation_regressor.pkl", "wb") as f:
#     pickle.dump(artifacts, f)

# print("Model training complete!")
# print("Saved:")
# print("models/cnn_vision_model.keras")
# print("models/valuation_regressor.pkl")