import uuid

class Car:
    def __init__(self, full_name: str, movie_title: str):
        self.full_name = full_name
        self.movie_title = movie_title

    def get_db_record(self):
        return {
            "id": uuid.uuid4(),
            "full_name": self.full_name,
            "movie_title": self.movie_title,
        }
