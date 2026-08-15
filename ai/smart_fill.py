import cv2
import numpy as np


class SmartFill:

    # Create the Smart Fill object
    def __init__(self):
        pass

    # Create a mask for the outer white background
    def generate_background_mask(self, template_img):

        # Stop if no image is received
        if template_img is None:
            return None

        # Get the image size
        height, width = template_img.shape[:2]

        # Convert the image into grayscale
        gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

        # Create a mask for flood fill
        background_mask = np.zeros((height + 2, width + 2), dtype=np.uint8)

        # Detect the white background
        _, white_area = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Use all four corners as the starting point
        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1)
        ]

        temp_image = white_area.copy()

        # Mark the outer white area
        for point in corners:

            if temp_image[point[1], point[0]] == 255:

                cv2.floodFill(
                    temp_image,
                    background_mask,
                    point,
                    128,
                    flags=4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE
                )

        # Create the final background mask
        outer_background = np.where(
            temp_image == 128,
            255,
            0
        ).astype(np.uint8)

        return outer_background

    # Fill only the selected closed region
    def fill_region(self, canvas, seed_point, color, background_mask=None):

        # Stop if canvas or point is missing
        if canvas is None or seed_point is None:
            return False

        x, y = seed_point
        height, width = canvas.shape[:2]

        # Check if the point is inside the image
        if not (0 <= x < width and 0 <= y < height):
            return False

        # Get the selected pixel color
        current_color = canvas[y, x]

        # Find the brightness of the selected pixel
        brightness = int(
            0.114 * int(current_color[0]) +
            0.587 * int(current_color[1]) +
            0.299 * int(current_color[2])
        )

        # Don't fill the black outline
        if brightness < 40:
            return False

        # Don't fill again if the same color is already there
        if np.array_equal(current_color, color):
            return False

        # Don't fill the outer white background
        if background_mask is not None:

            if background_mask[y, x] == 255:
                return False

        # Create a temporary mask to check the fill area
        test_mask = np.zeros((height + 2, width + 2), dtype=np.uint8)

        filled_pixels, _, _, _ = cv2.floodFill(
            canvas.copy(),
            test_mask,
            (x, y),
            color,
            loDiff=(20, 20, 20),
            upDiff=(20, 20, 20),
            flags=4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE
        )

        # Stop if nothing was filled
        if filled_pixels <= 0:
            return False

        # Make sure the color doesn't leak outside the drawing
        if background_mask is not None:

            filled_area = test_mask[1:height + 1, 1:width + 1]

            if np.any(
                (filled_area > 0) &
                (background_mask == 255)
            ):
                return False

        # Create the real mask
        real_mask = np.zeros((height + 2, width + 2), dtype=np.uint8)

        # Fill the selected region
        cv2.floodFill(
            canvas,
            real_mask,
            (x, y),
            color,
            loDiff=(20, 20, 20),
            upDiff=(20, 20, 20),
            flags=4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE
        )

        return True

    # Call the fill function from other files
    def fill(self, image, seed_point, fill_color, background_mask=None):

        # Create a copy so the original image is not changed
        canvas_copy = image.copy()

        # Apply Smart Fill
        success = self.fill_region(
            canvas_copy,
            seed_point,
            fill_color,
            background_mask
        )

        # Return the filled image if successful
        if success:
            return canvas_copy

        return image


# Create one Smart Fill object that can be used anywhere
smart_fill = SmartFill()


# This function is called from api.py
def apply_smart_fill(image, seed_point, fill_color, background_mask=None):

    return smart_fill.fill(
        image,
        seed_point,
        fill_color,
        background_mask
    )