from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import sys
sys.path.append("/home/reemarani/work/test_poc/test_backend")
from config.config import Database
from database.DatabaseParent import DatabaseParent
from database.models import AddPerson, AddCamera


class TrackDB(DatabaseParent):
    def __init__(self) -> None:
        self.persons = Database.PERSON_COL
        self.cameras = Database.CAMERA_COL
        self.tracks = Database.TRACK_COL
        self.images = Database.IMAGES_COL
        self.encodings = Database.IMAGES_COL
        
        super().__init__(db_name=Database.DB_NAME, persons=self.persons, cameras=self.cameras, tracks=self.tracks, images=self.images, encodings=self.encodings)
        # super().__init__(db_name=Database.DB_NAME, col_name=col_name)

    def add_person(self,
                   img_path: str,
                   img_name: str
                   ):

        data = {  # AddPerson(
            "img_path": img_path,
            "img_name": img_name,
            "timestamp": datetime.now().isoformat()
            # )
        }
        print(f"data: {data}")
        resp = self.persons_col.insert_one(data)
        return resp.acknowledged

    # to add the details of an indiviual camera
    # def add_camera(self, camera):
    #     self.cameras.insert_one({
    #         'name': camera.name,
    #         'ip': camera.ip,
    #         'port': camera.port
    #     })
    def add_camera(self,
                   camera_id: str,
                   camera_name: str,
                   camera_path: str):
        # data = AddCamera(
        #     camera_name=camera_name,
        #     camera_path=camera_path,
        #     timestamp=datetime.now().isoformat()
        # )
        data = {  # AddPerson(
            "camera_id": camera_id,
            "camera_name": camera_name,
            "camera_path": camera_path,
            "timestamp": datetime.now().isoformat()
            # )
        }
        print(f"data: {data}")
        resp = self.cameras_col.insert_one(data)
        return resp.acknowledged

    # to add the details of an indiviual track for a camera
    # def add_track(self, encoding_id, camera_id, date, time):
    #     _id = self.tracks.insert_one({
    #         'encoding_id': encoding_id,
    #         'camera_id': camera_id,
    #         'kind': 'login',
    #         'time': time,
    #         'date': date
    #     }).inserted_id
    #     return str(_id)
    def add_track(self, person_id: str,
                  camera_id: str):
        _id = self.tracks_col.insert_one({
            'person_id': person_id,
            'camera_id': camera_id,
            "timestamp": datetime.now().timestamp()
            # 'date': datetime.now().date().isoformat(),
            # 'time': datetime.now().time().isoformat()
        }).inserted_id
        return str(_id)

    # to add the images of an indiviual person
    def add_image(self, encoding_id, track_id):
        _id = self.images_col.insert_one({
            'encoding_id': encoding_id,
            'track_id': track_id

        }).inserted_id
        return str(_id)

    # to fetch data of every person
    def get_persons(self):
        persons = self.persons_col.find()
        result = []
        for person in persons:
            person['_id'] = str(person['_id'])
            person['id'] = person.pop('_id')
            result.append(person)
        return result

    # to fetch data of every camera
    def get_cameras(self):
        cameras = self.cameras_col.find({})
        result = []
        for camera in cameras:
            camera['_id'] = str(camera['_id'])
            camera['id'] = camera.pop('_id')
            result.append(camera)
        return result

    # to create track model for every person in camera (save location of every frame in which person is present)
    def __create_track_model(self, track):
        track['camera'] = self.get_camera(track['camera_id'])
        image = self.get_image_for_track(track['id'])
        track['image'] = image

        encoding = self.get_encoding(track['encoding_id'])
        encoding_person_id = encoding['person_id']

        if encoding_person_id:
            track['person'] = self.get_person(encoding_person_id)
        else:
            track['person'] = {
                'id': track['encoding_id'],
                'firstName': 'Anonymous',
                'lastName': 'Anonymous',
                'age': '',
                'height': '',
                'description': ''
            }
        track.pop('camera_id')

        return track

        # to fetch data of every camera

    def get_tracks(self):
        tracks = self.tracks_col.find({})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            # result.append(self.__create_track_model(track))
            result.append(track)
        return result

    def get_tracks_for_person(self, person_id):
        tracks = self.tracks_col.find({'person_id': person_id})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(track)
        return result

    # to fetch location of camera in which a person is tracked
    def get_tracks_for_camera(self, camera_id):
        tracks = self.tracks_col.find({'camera_id': camera_id})
        result = []
        for track in tracks:
            track['_id'] = str(track['_id'])
            track['id'] = track.pop('_id')
            result.append(track)
        return result

    # to fetch the details of an indiviual person
    def get_person(self, id):
        person = self.persons_col.find_one({'_id': ObjectId(id)})
        if person:
            person['_id'] = str(person['_id'])
            person['id'] = person.pop('_id')
            return person
        else:
            return None

    # to fetch the details of an indiviual camera
    def get_camera(self, id):
        camera = self.cameras_col.find_one({'_id': ObjectId(id)})
        camera['_id'] = str(camera['_id'])
        camera['id'] = camera.pop('_id')
        return camera

    # to fetch the details of an indiviual track
    def get_track(self, id):
        track = self.tracks_col.find_one({'_id': ObjectId(id)})
        track['_id'] = str(track['_id'])
        track['id'] = track.pop('_id')
        return self.__create_track_model(track)

    # to fetch the track details of an indiviual image of a person
    def get_image_for_track(self, track_id):
        image = self.images_col.find_one({'track_id': track_id})
        return str(image['_id'])

    # to fetch all the images of an indiviual person
    def get_images_for_person(self, person_id):
        encoding_for_person = self.get_encoding_for_person(person_id)

        if encoding_for_person:
            images = self.images_col.find({'encoding_id': encoding_for_person['id']})
            result = []
            for image in images:
                result.append(str(image['_id']))
            return result

        else:
            return []

    # to fetch all the images of all person
    def get_all_person_images(self):
        images = self.images_col.aggregate([
            {
                "$group":
                    {
                        "_id": "$encoding_id",
                        "images": {"$first": "$_id"}
                    }
            }
        ])
        result = {}
        for image in images:
            encoding = self.get_encoding(str(image['_id']))
            encoding_person_id = encoding['person_id']

            if encoding_person_id:
                result[encoding_person_id] = str(image['images'])
            else:
                continue

        return result

    ############## to add the details of an indiviual person
    # def add_person(self, person):
    #     self.persons.insert_one({
    #         'firstName': person.first_name,
    #         'lastName': person.last_name,
    #         'age': person.age,
    #         'height': person.height,
    #         'description': person.description
    #     })

    # to edit the details of an indiviual person
    def edit_person(self, person):
        query = {'_id': ObjectId(person.id)}
        new_values = {
            '$set': {
                'firstName': person.first_name,
                'lastName': person.last_name,
                'age': person.age,
                'height': person.height,
                'description': person.description
            }
        }

        self.persons_col.update_one(query, new_values)

    # to edit the details of an indiviual camera
    def edit_camera(self, camera):
        query = {'_id': ObjectId(camera.id)}
        new_values = {
            '$set': {
                'name': camera.name,
                'ip': camera.ip,
                'port': camera.port
            }
        }
        self.cameras_col.update_one(query, new_values)

    # to edit the details of an indiviual track
    def edit_track(self, track):
        query = {'_id': ObjectId(track.id)}
        encoding_for_person = self.get_encoding_for_person(track.person_id)
        if encoding_for_person:
            self.edit_encoding(encoding_for_person['id'], track.person_id)
        else:
            self.edit_encoding(track.encoding_id, track.person_id)

    # to delete the details of an indiviual person
    def delete_person(self, id):
        query = {'_id': ObjectId(id)}
        self.persons_col.delete_one(query)

    # to delete the details of an indiviual camera
    def delete_camera(self, id):
        query = {'_id': ObjectId(id)}
        self.cameras_col.delete_one(query)

    # to delete the details of an indiviual track
    def delete_track(self, id):
        query = {'_id': ObjectId(id)}
        self.tracks_col.delete_one(query)

    # to delete the image of an indiviual person
    def delete_image(self, id):
        query = {'_id': ObjectId(id)}
        self.images_col.delete_one(query)

    # to get all the encodings for images of all person
    def get_encodings(self):
        encodings = self.encodings_col.find({})
        result = []
        for encoding in encodings:
            encoding['_id'] = str(encoding['_id'])
            encoding['id'] = encoding.pop('_id')
            result.append(encoding)
        return result

    # to get the encodings for image of an indiviual person
    def get_encoding(self, id):
        encoding = self.encodings_col.find_one({'_id': ObjectId(id)})
        encoding['_id'] = str(encoding['_id'])
        encoding['id'] = encoding.pop('_id')
        return encoding

    # to get all the encodings for all the images of an indiviual person
    def get_encoding_for_person(self, person_id):
        encoding = self.encodings_col.find_one({'person_id': person_id})
        if encoding:
            encoding['_id'] = str(encoding['_id'])
            encoding['id'] = encoding.pop('_id')
            return encoding
        else:
            return None

    # to add encodings for image of an indiviual person
    def add_encoding(self, encoding, camera_id):
        _id = self.encodings_col.insert_one({
            'encoding': encoding,
            'person_id': None,
            'camera_id': camera_id
        }).inserted_id
        return str(_id)

    # to edit the person id in the encodings for image of an indiviual person
    def edit_encoding(self, encoding_id, person_id):
        query = {'_id': ObjectId(encoding_id)}
        new_values = {
            '$set': {
                'person_id': person_id,
            }
        }
        self.encodings_col.update_one(query, new_values)

    # to update the encodings for image of an indiviual person
    def update_encoding(self, encoding_id, encoding):
        query = {'_id': ObjectId(encoding_id)}
        new_values = {
            '$set': {
                'encoding': encoding,
            }
        }
        self.encodings_col.update_one(query, new_values)

    def delete_one_person(self, image_name: str):
        # for x in _out:
        self.persons_col.delete_one({"img_name": image_name})
        return True

    def delete_all_persons(self):
        _out = self.persons_col.find()
        for x in _out:
            self.persons_col.delete_one(x)
        return True

    def delete_all_cameras(self):
        _out = self.cameras_col.find()
        for x in _out:
            self.cameras_col.delete_one(x)
        return True


if __name__ == "__main__":
    obj = TrackDB()
    print(obj.get_persons())
    obj.add_camera(camera_id="2", camera_name="CAM02", camera_path="/home/reemarani/Desktop/input/videos/production ID_4881727.mp4")
