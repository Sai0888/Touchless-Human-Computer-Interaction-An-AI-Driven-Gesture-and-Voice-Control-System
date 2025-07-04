import cv2
import mediapipe as mp
import numpy as np
import speech_recognition as sr
import threading
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Audio Control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

last_hand_time = time.time()
voice_active = False  # Flag to avoid multiple voice listening

def calculate_distance(lm1, lm2):
    return np.sqrt((lm1.x - lm2.x) ** 2 + (lm1.y - lm2.y) ** 2)

def listen_for_command():
    global voice_active
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()

            if "increase volume" in command:
                level = min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0)
                volume.SetMasterVolumeLevelScalar(level, None)
            elif "decrease volume" in command:
                level = max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0)
                volume.SetMasterVolumeLevelScalar(level, None)
            elif "increase brightness" in command:
                current = sbc.get_brightness(display=0)[0]
                level = min(current + 5, 100)
                sbc.set_brightness(level)
            elif "decrease brightness" in command:
                current = sbc.get_brightness(display=0)[0]
                level = max(current - 5, 0)
                sbc.set_brightness(level)

        except Exception as e:
            print("Command not recognized.", str(e))

    voice_active = False  # Reset voice flag

# Initialize camera
cap = cv2.VideoCapture(0)

# Resize window smaller at start
cv2.namedWindow("Gesture & Voice Control", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Gesture & Voice Control", 800, 600)

# Print to console
print("Initializing Gesture & Voice Control System...")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    left_hand, right_hand = False, False

    if results.multi_hand_landmarks:
        last_hand_time = time.time()  # Update last hand detection time
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            distance = calculate_distance(thumb_tip, index_tip)

            # Adjust sensitivity
            if handedness == "Left":
                left_hand = True
                volume_level = np.interp(distance, [0.02, 0.18], [0.0, 1.0])
                volume.SetMasterVolumeLevelScalar(volume_level, None)
                cv2.putText(frame, f"Volume: {int(volume_level * 100)}%", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif handedness == "Right":
                right_hand = True
                brightness_level = int(np.interp(distance, [0.02, 0.18], [0, 100]))
                sbc.set_brightness(brightness_level)
                cv2.putText(frame, f"Brightness: {brightness_level}%", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if not left_hand and not right_hand and not voice_active and (time.time() - last_hand_time > 3):
        voice_active = True
        threading.Thread(target=listen_for_command, daemon=True).start()

    if not left_hand:
        cv2.putText(frame, "Show LEFT Hand for Volume", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    if not right_hand:
        cv2.putText(frame, "Show RIGHT Hand for Brightness", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.putText(frame, "Press 'Q' to Quit", (950, 650),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Gesture & Voice Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
