import cv2
import face_recognition
import numpy as np
from mongodb_face_detection import get_face_data

# Load known face data from MongoDB
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

known_face_encodings, known_face_names = get_face_data()


def process_video(input_video_path, output_video_path):
    video_capture = cv2.VideoCapture(input_video_path)

    # Get video properties
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Write the resulting frame to the output video
        out.write(frame)

    video_capture.release()
    out.release()
