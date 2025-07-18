# test_cam.py
import cv2

cap = cv2.VideoCapture(0)  # Try changing to 1, 2, 3

if not cap.isOpened():
    print("Camera not found.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    cv2.imshow("Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
