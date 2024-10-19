from typing import List, override
from cassandra.cluster import Cluster
import uuid
from .db import Db
from .model.car import Car


class Scylla(Db):
    def __init__(self):
        self.cluster = Cluster(
                contact_points= [
                    "127.0.0.1",
                    ]
                )

        self.session = self.cluster.connect()

    @staticmethod
    def __parse_car(car: Car) -> dict:
        return {
            "id": uuid.uuid4(),
            "full_name": car.full_name,
            "movie_title": car.movie_title,
        }

    @override
    def insert_element(self, car: Car):
        db_car = Scylla.__parse_car(car)
        query = self.session.prepare("""
            INSERT INTO sdb.car (id, full_name, movie_title) VALUES (?, ?, ?)
        """)
        self.session.execute(query, db_car.values())

    @override
    def insert_elements(self, cars: List[Car]):
        query = self.session.prepare("""
                INSERT INTO sdb.car (id, full_name, movie_title) VALUES (?, ?, ?)
            """)
        for car in cars:
            db_car = Scylla.__parse_car(car)
            self.session.execute(query, db_car.values())
