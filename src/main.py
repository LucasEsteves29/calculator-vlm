import cv2
import mediapipe as mp

def count_fingers(thumb, index, middle, ring, pinky, number=0):
    """
    Return the number of extended fingers based on coordinate differences.

    Parameters represent relative positional differences of finger joints.
    When the difference exceeds an empirically defined threshold,
    the corresponding finger is considered “raised/up”.
    """
    if abs(thumb) >= 0.15:   # Thumb: absolute difference on x-axis due to its lateral movement
        number += 1
    
    if index >= 0.15:       # Index finger: vertical difference threshold
        number += 1
    
    if middle >= 0.20:      # Middle finger: slightly higher threshold for stability
        number += 1
    
    if ring >= 0.18:        # Ring finger threshold
        number += 1
    
    if pinky >= 0.09:       # Pinky: smallest threshold due to shorter length
        number += 1

    return number


def calculate_fingers(handlms):
    """
    Compute coordinate differences between finger landmarks and detect
    whether each finger is extended.

    The mediapipe hand model indexes finger joints sequentially.
    Differences between fingertip and proximal joints are used to determine
    relative finger extension.
    """
    thumb  = handlms.landmark[4].x  - handlms.landmark[9].x
    index  = handlms.landmark[5].y  - handlms.landmark[8].y
    middle = handlms.landmark[9].y  - handlms.landmark[12].y
    ring   = handlms.landmark[13].y - handlms.landmark[16].y
    pinky  = handlms.landmark[17].y - handlms.landmark[20].y

    return count_fingers(thumb, index, middle, ring, pinky)


def show_fingers(fingers, coordinates):
    """
    Display the number of fingers detected as extended and draw
    hand landmarks on the frame for visual feedback.

    coordinates: tuple representing the position on the window where
    the counter will be displayed.
    """
    cv2.putText(frame, str(fingers), coordinates,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA)
    
    mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)


mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,        # Enables real-time tracking
    max_num_hands=2,                # Detect up to 2 hands
    model_complexity=1,             # Default model complexity
    min_detection_confidence=0.6,   # Detection threshold
    min_tracking_confidence=0.6     # Tracking threshold
) as hands:

    # Main capture loop for real-time video processing
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)                # Mirrors camera image for natural interaction
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)              # Hand landmark detection

        lresult = 0
        rresult = 0

        if results.multi_hand_landmarks:
            for i, hand_lms in enumerate(results.multi_hand_landmarks):
                
                # Identify whether the detected hand is left or right
                hand_label = results.multi_handedness[i].classification[0].label     

                if hand_label == 'Left':
                    lresult = calculate_fingers(hand_lms)
                    show_fingers(lresult, (10, 30))

                if hand_label == 'Right':
                    rresult = calculate_fingers(hand_lms)
                    show_fingers(rresult, (600, 30))

                # If both hands detected, display combined total fingers
                if rresult and lresult:
                    final_result = f"{int(lresult) + int(rresult)} fingers!"
                    cv2.putText(frame, str(final_result), (230, 470),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 255, 255),
                                2,
                                cv2.LINE_AA)

        cv2.imshow("Hands", frame)

        # Press 'q' to stop execution safely
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
