# face_utils.py
import cv2
import face_recognition
import json
import numpy as np
import time

def capture_multiple_encodings(num_captures=5, delay=1.5):
    cam = cv2.VideoCapture(0)
    print("Hệ thống sẽ tự động chụp 5 lần khi phát hiện khuôn mặt...")

    encodings = []
    count = 0
    start_time = time.time()

    while count < num_captures:
        ret, frame = cam.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            elapsed = time.time() - start_time
            if elapsed >= delay:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
                encodings.append(json.dumps(face_encoding.tolist()))
                count += 1
                print(f"Đã chụp {count}/{num_captures}")
                start_time = time.time()

        msg = f"Đang chụp tự động ({count}/{num_captures})..."
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Đăng ký khuôn mặt", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return encodings

def compare_face(current_encoding_json, known_encodings):
    current_encoding = np.array(json.loads(current_encoding_json))

    for user in known_encodings:
        known_encoding = np.array(json.loads(user['face_encoding']))
        result = face_recognition.compare_faces([known_encoding], current_encoding, tolerance=0.45)
        if result[0]:
            return user['name'], user['id']
    return None, None
