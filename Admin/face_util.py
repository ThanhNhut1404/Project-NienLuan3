import face_recognition
import numpy as np
import json

def extract_face_encodings_from_frame(frame):
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        return None
    encodings = face_recognition.face_encodings(frame, face_locations)
    if not encodings or len(encodings[0]) != 128:
        return None
    return encodings[0].tolist()

def compare_face(new_encoding, known_encodings_list, tolerance=0.6):
    try:
        new_encoding_array = np.array(new_encoding, dtype=np.float64)
        if new_encoding_array.shape != (128,):
            print(f"[Lỗi] encoding mới không hợp lệ: {new_encoding_array.shape}")
            return False
    except Exception as e:
        print(f"[Lỗi] Không thể chuyển encoding mới: {e}")
        return False

    try:
        for known in known_encodings_list:
            if isinstance(known, str):
                try:
                    known = json.loads(known)
                except Exception as e:
                    print(f"[Lỗi] Không thể parse encoding: {e}")
                    continue

            known_array = np.array(known, dtype=np.float64)
            if known_array.shape != (128,):
                print("[Bỏ qua] Encoding sai kích thước:", known)
                continue

            match_result = face_recognition.compare_faces([known_array], new_encoding_array, tolerance)
            if isinstance(match_result, list) and any(match_result):
                return True
    except Exception as e:
        print(f"[Lỗi] So sánh khuôn mặt: {e}")

    return False
