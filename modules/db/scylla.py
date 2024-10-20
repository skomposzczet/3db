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
    def insert_element(self, car: Car) -> str:
        db_car = Scylla.__parse_car(car)
        query = self.session.prepare("""
            INSERT INTO sdb.car (id, full_name, movie_title) VALUES (?, ?, ?)
        """)
        self.session.execute(query, db_car.values())
        return str(db_car["id"])

    @override
    def insert_elements(self, cars: List[Car]) -> str:
        query = self.session.prepare("""
                INSERT INTO sdb.car (id, full_name, movie_title) VALUES (?, ?, ?)
            """)
        for car in cars[:-1]:
            db_car = Scylla.__parse_car(car)
            self.session.execute(query, db_car.values())
        return self.insert_element(cars[-1])

    @override
    def update_element(self, uid: str, new_full_name: str):
        query = self.session.prepare("""
            UPDATE sdb.car SET full_name = ? WHERE id = ?
        """)
        self.session.execute(query, [new_full_name, uuid.UUID(uid)])
