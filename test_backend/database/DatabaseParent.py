from pymongo import MongoClient
from typing import List
from config import Database


class DatabaseParent(MongoClient):
    """
    Parameter
    ----------
    db_name:str --> mongodb database name
    col_name:str --> mongodb collection name

    **Note:**
    *Do not call class directly \n
    *Do not modify until necessary

    """

    def __init__(self, db_name, persons, cameras, tracks, images, encodings) -> None:
        self._host = Database.HOST
        self._port = Database.PORT
        super().__init__(
            host=self._host,
            port=self._port,
        )
        self.db = self[db_name]
        # self.col = self.db[col_name]
        self.persons_col = self.db[persons]
        self.cameras_col = self.db[cameras]
        self.tracks_col = self.db[tracks]
        self.images_col = self.db[images]
        self.encodings_col = self.db[encodings]
