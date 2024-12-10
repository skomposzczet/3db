import uuid


class Car:
    def __init__(self,
                 full_name: str,
                 car_brand: str,
                 car_class: str,
                 movie_title: str,
                 movie_type: str
                 ):
        self.uuid = uuid.uuid4()
        self.full_name = str(full_name)
        self.car_brand = str(car_brand)
        self.car_class = str(car_class)
        self.movie_title = str(movie_title)
        self.movie_type = str(movie_type)

    def get_db_record(self):
        return {
            "id": self.uuid,
            "full_name": self.full_name,
            "car_brand": self.car_brand,
            "car_class": self.car_class,
            "movie_title": self.movie_title,
            "movie_type": self.movie_type,
        }
