import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import imutils
import time
from imutils.video import FPS
import sys
sys.path.append("/home/reemarani/work/test_poc/test_backend")
from config.config import PathConfig, FaceBlurConfig
from database.track_db import TrackDB
from typing import List

db = TrackDB()

start_time = FaceBlurConfig.start_time
end_time = FaceBlurConfig.end_time
count1 = FaceBlurConfig.count1
count2 = FaceBlurConfig.count2


# images = []
# personNames = []


def get_person_image_from_db(person_ids: List[str]):
    # Retrieve the person's image from the database based on the person_id
    person_dictionary = {}
    for person_id in person_ids:
        person_data = db.get_person(id=person_id)
        if person_data:
            # encoded_image = person_data['image']
            # nparr = np.frombuffer(base64.b64decode(encoded_image), np.uint8)
            # person_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # person_image = person_data['image_path']
            person_dictionary[person_data["id"]] = person_data["img_path"]
    print(f"person_dictionary: {person_dictionary}")
    return person_dictionary


def faceEncodings(images: str):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def track_person_in_video(video_id, video_path, person_ids):
    time.sleep(2)
    # path = []
    # for person_id in person_ids:
    target_person_image = get_person_image_from_db(person_ids)
    print(f"target_person_: {target_person_image}")
    # path.append(target_person_image)

    if target_person_image is None:
        print("Person not found in the database.")
        return

    global start_time, count1, \
        count2, end_time
    personNames = []
    images = []
    for person_id, image_path in target_person_image.items():
        current_Img = cv2.imread(image_path)
        images.append(current_Img)
        personNames.append(person_id)

    print()
    # print(f"images: {images}")
    print(f"person names2: {personNames}")
    print()

    encodeListKnown = faceEncodings(images=images)
    print(f"video_path: {video_path}")
    # print(f"encodelistknown: {encodeListKnown}")
    cap = cv2.VideoCapture(video_path)
    print(f"cap: {cap.isOpened()}")
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    file_name_ext = f'{video_path.split(".")[0].split("/")[-1]}.webm'
    output_file = os.path.join(PathConfig.BASE_DIR, PathConfig.OUT_DIR, file_name_ext)
    fps1 = int(cap.get(cv2.CAP_PROP_FPS))
    result = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'vp80'), fps1,
                             (frame_width, frame_height))

    fps = FPS().start()
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"frames: {frames}")
    fps1 = int(cap.get(cv2.CAP_PROP_FPS))  # calculate duration of the video
    seconds = int(frames / fps1)
    if not cap.isOpened():
        print("Error reading cap file")
        return False, 'Error reading cap file'
    else:
        c = 0
        try:
            while True:
                c += 1
                print(c)
                ret, frame = cap.read()
                if not ret:
                    break
                # frame = cap.read()
                frame = imutils.resize(frame, width=800)
                faces = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                facesCurrentFrame = face_recognition.face_locations(faces)
                encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

                for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    print(faceDis)
                    matchIndex = np.argmin(faceDis)
                    print(personNames)

                    if matches[matchIndex]:
                        id_name = personNames[matchIndex]
                        if count1 == 0:
                            count1 += 1
                            start_time = str(timedelta(seconds=seconds) - timedelta(seconds=5))
                        end_time = str(timedelta(seconds=seconds))
                        print(f"id_name {id_name}")

                        y1, x2, y2, x1 = faceLoc
                        # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        time.sleep(5)
                        # Update the MongoDB with the output video path
                        db.add_track(person_id=id_name, camera_id=video_id)

                result.write(cv2.resize(frame, size))
                frame = cv2.imencode('.jpg', frame)[1].tobytes()
                # cv2.imshow('video', frame)
                fps.update()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                # if cv2.waitKey(10) == ord('q'):
                #     break
            cap.release()
            result.release()
            # cv2.destroyAllWindows()
            print(f"INFO: The video was successfully saved to {output_file} ")
            return True, os.path.join(PathConfig.OUT_DIR, file_name_ext)

        except Exception as e:
            print(e)
            if start_time != 0:
                print("Person between" + str(start_time) + "to" + str(end_time))
            else:
                print("Person not found!")
            return False, str(e)


if __name__ == "__main__":
    print(track_person_in_video(video_id="abc",
                                video_path="/home/reemarani/work/test_poc/test_backend/input/videos/production "
                                           "ID_4881727.mp4",
                                person_ids=["64cb21ea8dff166dedaecc97"]))
