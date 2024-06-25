import face_recognition
import cv2

cap = cv2.VideoCapture("/home/reemarani/work/test_poc/test_backend/input/videos/production ID_4881727.mp4")
count = 1

while True:
    ret, frame = cap.read()
    print(f"ret: {ret}")
    if not ret:
        break
    # frame = cap.read()
    count += 1
    print(f"processed count: {count}")
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"count: {count}")
