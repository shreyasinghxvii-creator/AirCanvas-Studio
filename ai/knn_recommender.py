import numpy as np
from sklearn.neighbors import NearestNeighbors


class KNNColorRecommender:

    def __init__(self):

        # Main colour families (RGB)
        self.family_names = [
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "pink",
            "brown",
            "black",
            "white"
        ]

        self.family_colors = np.array([
            [239, 68, 68],      # Red
            [249, 115, 22],     # Orange
            [250, 204, 21],     # Yellow
            [34, 197, 94],      # Green
            [59, 130, 246],     # Blue
            [168, 85, 247],     # Purple
            [236, 72, 153],     # Pink
            [139, 90, 43],      # Brown
            [0, 0, 0],          # Black
            [255, 255, 255]     # White
        ])

        # Train KNN using colour families
        self.knn = NearestNeighbors(
            n_neighbors=1,
            algorithm="ball_tree"
        )

        self.knn.fit(self.family_colors)

        # Suggested shades for every family
        self.family_recommendations = {

            "red": [
                "#f97316",   # Orange
                "#dc2626",   # Crimson
                "#ec4899",   # Pink
                "#7f1d1d"    # Maroon
            ],

            "orange": [
                "#facc15",   # Yellow
                "#fb923c",   # Light Orange
                "#ef4444",   # Red
                "#f59e0b"    # Gold
            ],

            "yellow": [
                "#eab308",   # Gold
                "#f97316",   # Orange
                "#84cc16",   # Lime
                "#fde68a"    # Cream
            ],

            "green": [
                "#22c55e",   # Emerald
                "#84cc16",   # Lime
                "#15803d",   # Dark Green
                "#14b8a6"    # Teal
            ],

            "blue": [
                "#60a5fa",   # Sky Blue
                "#06b6d4",   # Cyan
                "#1e40af",   # Navy
                "#a855f7"    # Purple
            ],

            "purple": [
                "#9333ea",   # Violet
                "#ec4899",   # Pink
                "#3b82f6",   # Blue
                "#c084fc"    # Lavender
            ],

            "pink": [
                "#ec4899",   # Pink
                "#f472b6",   # Light Pink
                "#a855f7",   # Purple
                "#ef4444"    # Red
            ],

            "brown": [
                "#92400e",   # Brown
                "#65a30d",   # Olive
                "#facc15",   # Yellow
                "#ef4444"    # Red
            ],

            "black": [
                "#6b7280",   # Grey
                "#374151",   # Dark Grey
                "#c0c0c0",   # Silver
                "#ffffff"    # White
            ],

            "white": [
                "#c0c0c0",   # Silver
                "#d1d5db",   # Light Grey
                "#3b82f6",   # Blue
                "#22c55e"    # Green
            ]
        }

    # Convert HEX to RGB
    def hex_to_rgb(self, hex_color):

        hex_color = hex_color.lstrip("#")

        return [
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        ]

    # Recommend colours
    def recommend(self, input_hex):

        try:

            rgb = self.hex_to_rgb(input_hex)

            # Find nearest colour family using KNN
            _, index = self.knn.kneighbors([rgb])

            family = self.family_names[index[0][0]]

            return self.family_recommendations.get(
                family,
                [
                    "#3b82f6",
                    "#22c55e",
                    "#f97316",
                    "#ec4899"
                ]
            )

        except Exception:

            return [
                "#3b82f6",
                "#22c55e",
                "#f97316",
                "#ec4899"
            ]