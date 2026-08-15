import os
import cv2
import numpy as np
from sklearn.cluster import KMeans


class KMeansPalette:

    # Set the default number of colors
    def __init__(self, default_k=5):
        self.default_k = default_k

    # Find the main colors from the image
    def extract_dominant_colors(self, image, k=None):

        if k is None:
            k = self.default_k

        if image is None or image.size == 0:
            return []

        # Convert image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert into pixel list
        pixels = image_rgb.reshape(-1, 3)

        # Remove very dark and very bright pixels
        brightness = (
            0.299 * pixels[:, 0] +
            0.587 * pixels[:, 1] +
            0.114 * pixels[:, 2]
        )

        valid_pixels = (brightness >= 40) & (brightness <= 220)

        filtered_pixels = pixels[valid_pixels]

        if len(filtered_pixels) < k:
            filtered_pixels = pixels

        # Run K-Means
        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        kmeans.fit(filtered_pixels)

        colors = kmeans.cluster_centers_
        labels = kmeans.labels_

        counts = np.bincount(labels)

        sorted_index = np.argsort(counts)[::-1]
        sorted_colors = colors[sorted_index]

        dominant_colors = []

        for color in sorted_colors:

            red = int(color[0])
            green = int(color[1])
            blue = int(color[2])

            dominant_colors.append((blue, green, red))

        return dominant_colors


# Create one extractor
palette_extractor = KMeansPalette()


# Colour palettes for different templates
TEMPLATE_PALETTES = {

    "car": [
        "#ef4444",  # Red
        "#3b82f6",  # Blue
        "#facc15",  # Yellow
        "#c0c0c0",  # Silver
        "#000000",  # Black
        "#ffffff"   # White
    ],

    "flower": [
        "#ec4899",  # Pink
        "#a855f7",  # Purple
        "#facc15",  # Yellow
        "#22c55e",  # Green
        "#ef4444"   # Red
    ],

    "butterfly": [
        "#3b82f6",  # Blue
        "#a855f7",  # Purple
        "#f97316",  # Orange
        "#facc15",  # Yellow
        "#ec4899"   # Pink
    ],

    "fish": [
        "#f97316",  # Orange
        "#3b82f6",  # Blue
        "#facc15",  # Yellow
        "#ffffff"   # White
    ],

    "tree": [
        "#22c55e",  # Green
        "#8b5a2b",  # Brown
        "#facc15",  # Yellow
        "#ef4444"   # Red
    ],

    "house": [
        "#ef4444",  # Roof
        "#8b5a2b",  # Brown
        "#3b82f6",  # Blue
        "#22c55e",  # Green
        "#ffffff"   # White
    ]
}


# Default colourful palette
DEFAULT_PALETTE = [
    "#ef4444",
    "#f97316",
    "#facc15",
    "#22c55e",
    "#3b82f6",
    "#a855f7"
]


# Used by api.py
def extract_palette(image_path, k=6):

    image = cv2.imread(image_path)

    if image is None:
        return []

    # Step 1 : Run K-Means
    colors = palette_extractor.extract_dominant_colors(image, k)

    palette = []
    gray_count = 0

    # Step 2 : Convert to HEX and count grayscale colours
    for blue, green, red in colors:

        if (
            abs(red - green) < 20 and
            abs(green - blue) < 20 and
            abs(red - blue) < 20
        ):
            gray_count += 1

        palette.append(f"#{red:02x}{green:02x}{blue:02x}")

    # Step 3 : If image is colourful, return K-Means result
    if gray_count < len(palette) * 0.7:
        return palette

    # Step 4 : Otherwise choose colours based on template name
    filename = os.path.basename(image_path).lower()

    for keyword, template_palette in TEMPLATE_PALETTES.items():
        if keyword in filename:
            return template_palette

    # Step 5 : If no template matched, return default palette
    return DEFAULT_PALETTE