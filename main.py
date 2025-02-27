import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize components
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Variables for blinking and scrolling
blink_start_time = 0
blink_count = 0
blink_timeout = 1  # Timeout period to detect multiple blinks (in seconds)
scroll_threshold = 0.02  # Threshold for gaze movement for scrolling
mouth_open_threshold = 0.05  # Threshold for mouth opening

# Helper functions
def is_blinking(left_eye):
    """Check if eyes are blinking based on vertical landmark distances."""
    return (left_eye[0].y - left_eye[1].y) < 0.004  # Adjust threshold if needed

def is_mouth_open(upper_lip, lower_lip):
    """Check if mouth is open based on lip landmarks."""
    return (lower_lip.y - upper_lip.y) > mouth_open_threshold

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmarks_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmarks_points:
        landmarks = landmarks_points[0].landmark

        # Highlight gaze tracking points
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                screen_x = min(max(int(landmark.x * screen_w), 30), screen_w - 30)
                screen_y = min(max(int(landmark.y * screen_h), 30), screen_h - 30)
                pyautogui.moveTo(screen_x, screen_y)

        # Detect blinking
        left_eye = [landmarks[145], landmarks[159]]  # Adjust indices for your dataset
        right_eye = [landmarks[374], landmarks[386]]  # Adjust indices for the right eye
        for landmark in left_eye + right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

        upper_lip = landmarks[13]
        lower_lip = landmarks[14]

        # Mouth and eyes detection logic
        mouth_open = is_mouth_open(upper_lip, lower_lip)
        left_eye_closed = is_blinking(left_eye)
        right_eye_closed = is_blinking(right_eye)

        # Debugging prints for conditions
        print(f"Mouth Open: {mouth_open}, Left Eye Closed: {left_eye_closed}, Right Eye Closed: {right_eye_closed}")

        if mouth_open:
            print("Go Back (Mouth Open)")
            pyautogui.hotkey('alt', 'left')
            time.sleep(1)  # Add a delay to prevent multiple triggers

        elif left_eye_closed and right_eye_closed and not mouth_open:
            print("Go Forward (Mouth and Eyes Closed)")
            pyautogui.hotkey('alt', 'right')
            time.sleep(1)  # Add a delay to prevent multiple triggers

        # Eye gaze scrolling logic
        gaze_y = landmarks[1].y  # Using the gaze point for vertical movement
        if left_eye_closed:
            if gaze_y < 0.5 - scroll_threshold:  # Looking upwards while blinking
                print("Scroll Up")
                pyautogui.scroll(300)  # Scroll up
            elif gaze_y > 0.5 + scroll_threshold:  # Looking downwards while blinking
                print("Scroll Down")
                pyautogui.scroll(-300)  # Scroll down

    cv2.imshow('Eye controlled cursor', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
