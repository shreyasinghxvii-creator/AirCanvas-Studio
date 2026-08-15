from flask import Blueprint, request, jsonify
import base64
import os
import cv2
import numpy as np

from ai.smart_fill import SmartFill
from ai.kmeans_palette import extract_palette
from ai.knn_recommender import KNNColorRecommender


# Create a blueprint for all API routes
api_bp = Blueprint("api", __name__)


# Create the Smart Fill object
smart_filler = SmartFill()

# Create the KNN Color Recommendation object
knn_recommender = KNNColorRecommender()


# Smart Fill API
@api_bp.route("/smart-fill", methods=["POST"])
def smart_fill():

    # Get all the data sent from the frontend
    data = request.json or {}

    # Get the image
    image_data = data.get("image")

    # Get the position where the user clicked
    x = int(data.get("x", 0))
    y = int(data.get("y", 0))

    # Get the selected color
    color_hex = data.get("color", "#000000")

    # Check if the image is received
    if not image_data:
        return jsonify({
            "status": "error",
            "message": "No image data provided"
        }), 400

    # Remove # from the HEX color
    hex_color = color_hex.lstrip("#")

    # Convert HEX color into BGR because OpenCV uses BGR
    bgr_color = tuple(int(hex_color[i:i + 2], 16) for i in (4, 2, 0))

    # Decode the base64 image
    image_bytes = base64.b64decode(image_data.split(",")[1])

    # Convert image into NumPy array
    image_array = np.frombuffer(image_bytes, np.uint8)

    # Convert NumPy array into OpenCV image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Apply Smart Fill
    filled_image = smart_filler.fill(image, (x, y), bgr_color)

    # Convert the filled image back into PNG
    _, buffer = cv2.imencode(".png", filled_image)

    # Convert PNG into base64
    encoded_image = base64.b64encode(buffer).decode("utf-8")

    # Send the filled image back to the frontend
    return jsonify({
        "status": "success",
        "image": f"data:image/png;base64,{encoded_image}"
    })


# Get the color palette from the selected template
@api_bp.route("/get-palette", methods=["POST"])
def get_palette():

    # Get the data from the frontend
    data = request.json or {}

    # Get the template path
    template_path = data.get("template_path", "")

    # Sanitize and resolve path relative to static directory
    filename = os.path.basename(template_path)
    real_path = os.path.join(api_bp.static_folder or "static", "templates", filename)

    # Fallback check if direct path exists or sanitized relative path exists
    target_path = template_path if os.path.exists(template_path) else real_path

    # Check if the template exists
    if os.path.exists(target_path):

        # Extract the dominant colors
        palette = extract_palette(target_path, k=6)

        return jsonify({
            "status": "success",
            "palette": palette
        })

    return jsonify({
        "status": "error",
        "message": f"Template file not found at {target_path}"
    }), 400


# Recommend matching colors using KNN
@api_bp.route("/recommend-colors", methods=["POST"])
def recommend_colors():

    # Get the selected color
    data = request.json or {}
    color_hex = data.get("color", "#FF0000")

    # Get similar colors
    recommendations = knn_recommender.recommend(color_hex)

    # Send the recommended colors
    return jsonify({
        "status": "success",
        "recommendations": recommendations
    })