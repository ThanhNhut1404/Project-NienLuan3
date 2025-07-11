import face_recognition
import numpy as np

def extract_face_encodings_from_frame(frame):
    """
    Trích xuất encoding từ frame (RGB).
    Trả về: list[float] nếu có khuôn mặt, ngược lại trả về None.
    """
    face_locations = face_recognition.face_locations(frame)
    if not face_locations:
        return None

    encodings = face_recognition.face_encodings(frame, face_locations)
    if not encodings:
        return None

    return encodings[0].tolist()


def compare_face(new_encoding, known_encodings_list, tolerance=0.6):
    """
    So sánh encoding mới (list) với danh sách encoding đã biết (list of list hoặc JSON string).
    Trả về True nếu trùng, ngược lại False.
    """
    try:
        new_encoding_array = np.array(new_encoding, dtype=np.float64)
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
            match = face_recognition.compare_faces([known_array], new_encoding_array, tolerance=tolerance)
            if match[0]:
                return True
    except Exception as e:
        print(f"[Lỗi] So sánh khuôn mặt: {e}")

    return False
