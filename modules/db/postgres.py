from typing import List, override
from modules.db.db import Db
from modules.db.model.car import Car
import psycopg2
from psycopg2 import sql
import uuid


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

    def select_id_from_table(self, table_name: str, id_name: str, elem_name: str, elem_value: str):
        query = sql.SQL("SELECT {id} from {table} WHERE {name} = %s").format(
            id=sql.Identifier(id_name), 
            table=sql.Identifier(table_name), 
            name=sql.Identifier(elem_name))
        self.cursor.execute(query, [str(elem_value)])

        return self.cursor.fetchone()

    def insert_new_element_to_table(self, table_name: str, id_name: str, elem_name: str, elem_value: str, elem_id: str):
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES (%s, %s)").format(
            table=sql.Identifier(table_name), 
            fields=sql.SQL(',').join([
                sql.Identifier(id_name),
                sql.Identifier(elem_name)]))

        self.cursor.execute(query, [elem_id, str(elem_value)])
    

    def get_element_id(self, table_name: str, id_name: str, elem_name: str, elem_value: str):
        elem_id = self.select_id_from_table(table_name, id_name, elem_name, elem_value)

        if (elem_id is not None):
            return str(elem_id[0])

        elem_id = str(uuid.uuid4())
        self.insert_new_element_to_table(table_name, id_name, elem_name, elem_value, elem_id)
        return elem_id


    def set_insert_query(self, record):
        brand_id = self.get_element_id("car_brands", "brand_id", "brand", record["car_brand"])
        class_id = self.get_element_id("car_classes", "class_id", "class", record["car_class"])
        title_id = self.get_element_id("movie_titles", "title_id", "title", record["movie_title"])
        type_id = self.get_element_id("movie_types", "type_id", "type_name", record["movie_type"])

        self.cursor.execute("""
            INSERT INTO car (id, full_name, brand_id, class_id, title_id, type_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [str(record["id"]), record["full_name"], brand_id, class_id, title_id, type_id])

    @override
    def insert_element(self, car: Car) -> str:
        record = car.get_db_record()
        self.set_insert_query(record)
        self.session.commit()
        return str(record["id"])

    @override
    def insert_elements(self, cars: List[Car]) -> str:
        for car in cars[:-1]:
            record = car.get_db_record()
            self.set_insert_query(record)
        return self.insert_element(cars[-1])

    @override
    def update_element(self, uid: str, new_full_name: str):
        self.cursor.execute("""
                UPDATE car SET full_name = %s WHERE id = %s
            """, [new_full_name, uid])
        self.session.commit()

    @override
    def delete_element(self, uid: str):
        self.cursor.execute("""
                DELETE from car WHERE id = %s
            """, [uid])
        self.session.commit()

    @override
    def select_element(self, uid: str):
        self.cursor.execute("""
                SELECT id, full_name, brand, class, title, type_name from car  
                INNER JOIN car_brands ON car.brand_id = car_brands.brand_id
                INNER JOIN car_classes ON car.class_id = car_classes.class_id
                INNER JOIN movie_titles ON car.title_id = movie_titles.title_id
                INNER JOIN movie_types ON car.type_id = movie_types.type_id
                WHERE id = %s
            """, [uid])
        return self.cursor.fetchone()
