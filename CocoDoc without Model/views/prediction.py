import streamlit as st
from PIL import Image
import numpy as np
import time
import tensorflow as tf
import json
import mysql.connector
from mysql.connector import Error
import gdown
import os

# Load the model
model_path = "trained_model/cocodoc_model.keras"  # Ensure the model path is correct
model = tf.keras.models.load_model(model_path)

# Google Drive file ID and link (use the ID from your Google Drive shareable link)
file_id = "1--9gO-E-XsoybOvvuA8LxnT7VkY88I75"  # Replace with actual file ID
download_url = f"https://drive.google.com/uc?id={file_id}"

# Check if model file exists, if not download it
if not os.path.exists(model_path):
    st.write("Model not found locally. Downloading from Google Drive...")
    gdown.download(download_url, model_path, quiet=False)
    
# Load the downloaded model
model = tf.keras.models.load_model(model_path)

# Load class indices
with open("trained_model/class_indices2.json") as json_file:
    class_indices = json.load(json_file)

# Reverse the class indices for easier lookup
class_indices_rev = {v: k for k, v in class_indices.items()}

def preprocess_image(image):
    """Preprocess the uploaded image for prediction."""
    # Resize the image to the size the model expects (adjust if necessary)
    image = image.resize((224, 224))  # Change to the input size your model requires
    image_array = np.array(image) / 255.0  # Scale pixel values to [0, 1]
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def create_connection():
    """Create a database connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  # Your host, usually localhost
        user="root",  # Your MySQL username
        password="Lakshan@2024",  # Your MySQL password
        database="cocodoc_db"  # Your database name
    )

def save_prediction_to_db(predicted_class, confidence, is_healthy, image_path):
    """Insert prediction data into the predictions table."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        # Convert numpy float to Python float
        confidence = float(confidence)
        
        # Insert a new record into the predictions table
        cursor.execute(
            """
            INSERT INTO predictions (image_path, predicted_class, confidence, timestamp, is_healthy)
            VALUES (%s, %s, %s, NOW(), %s)
            """,
            (image_path, predicted_class, confidence, is_healthy)
        )
        conn.commit()  # Commit the transaction
        cursor.close()
        conn.close()
        st.success("Prediction saved to database.")
    except Error as e:
        st.error(f"Error while inserting to database: {e}")

def render():
    st.title("Coconut Leaf Disease Prediction")

    st.write("""
    Upload an image of a coconut leaf to predict potential diseases.
    Make sure the image is clear and properly oriented for better results.
    """)

    # Example form for prediction input
    with st.form(key='prediction_form'):
        st.subheader("Upload Leaf Image for Prediction")

        # Upload image
        leaf_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if leaf_image:
            image = Image.open(leaf_image)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Submit button
        submit_button = st.form_submit_button("Predict")

        if submit_button:
            if leaf_image:
                st.write("Processing your prediction...")
                time.sleep(2)  # Simulate a processing delay

                # Preprocess the image
                processed_image = preprocess_image(image)

                # Make prediction
                predictions = model.predict(processed_image)
                predicted_class_index = np.argmax(predictions[0])  # Get index of the highest score

                # Debugging print statements
                st.write("Predictions:", predictions)
                st.write("Predicted class index:", predicted_class_index)

                predicted_class = class_indices_rev.get(predicted_class_index, "Unknown")
                confidence = np.max(predictions[0])  # Get the confidence score

                # Check if the predicted class is a coconut leaf disease
                valid_disease_classes = ['WCLWD', 'CCI', 'Healthy Leaves']  # Define valid prefixes

                # Check if the predicted class matches any of the valid prefixes
                is_healthy = 1 if predicted_class == "Healthy Leaves" else 0  # Set healthy flag

                if any(predicted_class.startswith(prefix) for prefix in valid_disease_classes):
                    st.success(f"Predicted disease for leaf is: **{predicted_class}**")
                    # Save to database
                    save_prediction_to_db(predicted_class, confidence, is_healthy, leaf_image.name)  # Use the file name as the image path
                else:
                    st.warning("You provided a non-coconut leaf image. Please upload a valid coconut leaf image.")
            else:
                st.warning("Please upload a leaf image for prediction.")
