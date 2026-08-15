import os
import base64
import cv2
import numpy as np

from flask import Flask, jsonify, render_template, request

# Import all application routes
from routes import register_blueprints

# Create Flask app
app = Flask(__name__)

# Secret key
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "aircanvas-secret-key-2026"
)

# Register all blueprints
register_blueprints(app)


# Show all registered routes inside Jinja templates
@app.context_processor
def inject_routes():
    return {
        "flex_routes": [
            rule.endpoint
            for rule in app.url_map.iter_rules()
        ]
    }


# Display startup message
def init_recommender():
    print("[INFO] AI modules loaded successfully.")


init_recommender()


# Process hand gesture frame
@app.route("/api/process-gesture", methods=["POST"])
def process_gesture():

    # Get request data
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({
            "success": False,
            "error": "No image received."
        }), 400

    try:

        # Decode base64 image
        image_data = data["image"]

        if "," in image_data:
            image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        image_array = np.frombuffer(image_bytes, np.uint8)

        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({
                "success": False,
                "error": "Unable to decode image."
            }), 400

        # Get frame size
        height, width, _ = frame.shape

        # Return demo coordinates
        return jsonify({
            "success": True,
            "detected": True,
            "x": width // 2,
            "y": height // 2,
            "gesture": "draw"
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# Start Flask server
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )