from typing import List, override
from modules.db.db import Db
from modules.db.model.car import Car
import psycopg2


class Postgres(Db):
    def __init__(self):
        self.session = psycopg2.connect(
            database='database',
            user='postgres',
            password='password',
            host='127.0.0.1',
            port='5432'
        )

        self.cursor = self.session.cursor()

    def __del__(self):
        self.session.close()

    @override
    def insert_element(self, car: Car) -> str:
        record = car.get_db_record()
        self.cursor.execute("""
            INSERT INTO car (id, full_name, movie_title)
            VALUES ('{id}', '{full_name}', '{movie_title}')
        """.format(**record))
        self.session.commit()
        return str(record["id"])

    @override
    def insert_elements(self, cars: List[Car]) -> str:
        for car in cars[:-1]:
            record = car.get_db_record()
            self.cursor.execute("""
                INSERT INTO car (id, full_name, movie_title)
                VALUES ('{id}', '{full_name}', '{movie_title}')
            """.format(**record))
        return self.insert_element(cars[-1])

    @override
    def update_element(self, uid: str, new_full_name: str):
        self.cursor.execute("""
                UPDATE car SET full_name = '{}' WHERE id = '{}'
            """.format(new_full_name, uid))
        self.session.commit()

    @override
    def delete_element(self, uid: str):
        self.cursor.execute("""
                DELETE from car WHERE id = '{}'
            """.format(uid))
        self.session.commit()

    @override
    def select_element(self, uid: str):
        self.cursor.execute("""
                SELECT * from car WHERE id = '{}'
            """.format(uid))
        return self.cursor.fetchone()
