import cv2
import mediapipe as mp
import threading
import pygame
import time
import csv
from datetime import datetime

# Alarm function
def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.wav")
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Indices for eyes (left and right)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def landmarks_to_point(landmark, shape):
    h, w = shape
    return (int(landmark.x * w), int(landmark.y * h))

def calculate_eye_aspect_ratio(eye_landmarks, shape):
    def euclidean(p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

    vertical1 = euclidean(eye_landmarks[1], eye_landmarks[5])
    vertical2 = euclidean(eye_landmarks[2], eye_landmarks[4])
    horizontal = euclidean(eye_landmarks[0], eye_landmarks[3])
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

# Start webcam
cap = cv2.VideoCapture(0)
eye_closed_frames = 0
alarm_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(frame_rgb)

    if result.multi_face_landmarks:
        mesh_points = result.multi_face_landmarks[0].landmark
        shape = frame.shape[:2]

        left_eye = [landmarks_to_point(mesh_points[i], shape) for i in LEFT_EYE]
        right_eye = [landmarks_to_point(mesh_points[i], shape) for i in RIGHT_EYE]

        left_ear = calculate_eye_aspect_ratio(left_eye, shape)
        right_ear = calculate_eye_aspect_ratio(right_eye, shape)
        avg_ear = (left_ear + right_ear) / 2

        # Draw eye mesh
        for pt in left_eye + right_eye:
            cv2.circle(frame, pt, 2, (0, 255, 0), -1)

        if avg_ear < 0.25:
            eye_closed_frames += 1
        else:
            eye_closed_frames = 0

        if eye_closed_frames > 15:  # About 1 second
            if not alarm_triggered:
                alarm_triggered = True
                threading.Thread(target=play_alarm).start()

                # ✅ Log the event with timestamp
                with open("drowsiness_log.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Drowsiness Detected!!"])

            cv2.putText(frame, "DROWSINESS ALERT!!", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            alarm_triggered = False

    cv2.imshow("Drowsiness Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
