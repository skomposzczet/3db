from typing import List, override
from cassandra.cluster import Cluster
from .db import Db
from .model.car import Car
import uuid


class Scylla(Db):
    def __init__(self):
        self.cluster = Cluster(
            contact_points=[
                "127.0.0.1",
                ]
            )

        self.session = self.cluster.connect()

    @override
    def insert_element(self, car: Car) -> str:
        db_car = car.get_db_record()
        query = self.session.prepare("""
            INSERT INTO
            sdb.car (id, full_name, car_brand, car_class, movie_title, type_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        self.session.execute(query, db_car.values())
        return str(db_car["id"])

    @override
    def insert_elements(self, cars: List[Car]) -> str:
        query = self.session.prepare("""
            INSERT INTO
            sdb.car (id, full_name, car_brand, car_class, movie_title, type_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        for car in cars[:-1]:
            db_car = car.get_db_record()
            self.session.execute(query, db_car.values())
        return self.insert_element(cars[-1])

    @override
    def update_element(self, uid: str, new_full_name: str):
        query = self.session.prepare("""
            UPDATE sdb.car SET full_name = ? WHERE id = ?
        """)
        self.session.execute(query, [new_full_name, uuid.UUID(uid)])

    @override
    def delete_element(self, uid: str):
        query = self.session.prepare("""
            DELETE from sdb.car WHERE id = ?
        """)
        self.session.execute(query, [uuid.UUID(uid)])

    @override
    def select_element(self, uid: str):
        query = self.session.prepare("""
            SELECT * from sdb.car WHERE id = ?
        """)
        return self.session.execute(query, [uuid.UUID(uid)])
