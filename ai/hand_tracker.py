import cv2
import mediapipe as mp


class HandTracker:

    # Create the hand tracker
    def __init__(self, max_hands=1, detection_con=0.7, track_con=0.7):

        # Load MediaPipe Hands
        self.mp_hands = mp.solutions.hands

        # Set the hand detection settings
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )

        # Store the previous finger position for smooth drawing
        self.prev_x = 0
        self.prev_y = 0

        # This value helps to reduce shaky hand movement
        self.alpha = 0.4

    # Process every webcam frame
    def process_frame(self, frame):

        # Get the height and width of the frame
        height, width, _ = frame.shape

        # Convert the frame from BGR to RGB because MediaPipe uses RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect the hand
        results = self.hands.process(rgb_frame)

        # By default nothing is detected
        is_drawing = False
        coordinates = None

        # Check if a hand is found
        if results.multi_hand_landmarks:

            # Get the first detected hand
            hand = results.multi_hand_landmarks[0]

            # Get all the landmarks of the hand
            landmarks = hand.landmark

            # Get the index finger tip and joint
            index_tip = landmarks[8]
            index_joint = landmarks[6]

            # Get the middle finger tip and joint
            middle_tip = landmarks[12]
            middle_joint = landmarks[10]

            # Check if the index finger is raised
            index_up = index_tip.y < index_joint.y

            # Check if the middle finger is down
            middle_down = middle_tip.y > middle_joint.y

            # Start drawing only when index finger is up
            if index_up and middle_down:

                is_drawing = True

                # Convert finger position into screen coordinates
                current_x = int(index_tip.x * width)
                current_y = int(index_tip.y * height)

                # For the first point use the original position
                if self.prev_x == 0 and self.prev_y == 0:

                    smooth_x = current_x
                    smooth_y = current_y

                else:

                    # Smooth the movement to reduce shaking
                    smooth_x = int(
                        self.alpha * current_x +
                        (1 - self.alpha) * self.prev_x
                    )

                    smooth_y = int(
                        self.alpha * current_y +
                        (1 - self.alpha) * self.prev_y
                    )

                # Save the current position
                self.prev_x = smooth_x
                self.prev_y = smooth_y

                # Return the smooth finger position
                coordinates = (smooth_x, smooth_y)

            else:

                # Reset the previous position
                self.prev_x = 0
                self.prev_y = 0

        else:

            # Reset if no hand is detected
            self.prev_x = 0
            self.prev_y = 0

        return is_drawing, coordinates