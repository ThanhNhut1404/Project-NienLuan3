import cv2

# Tải mô hình phát hiện khuôn mặt Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Mở webcam (0 là webcam mặc định)
cap = cv2.VideoCapture(0)

while True:
    # Đọc frame từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc dữ liệu từ webcam.")
        break

    # Chuyển sang ảnh xám để nhận diện khuôn mặt
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Vẽ hình chữ nhật quanh khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị khung hình có khuôn mặt
    cv2.imshow('Face Detection - Press Q to Quit', frame)



    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
