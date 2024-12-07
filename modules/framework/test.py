from modules.db.db import Db
from modules.framework.timer import Timer
from modules.framework.parser import DataProvider
from modules.db.model.car import Car
from pathlib import Path
import json


class Test:
    NUM_OF_ROWS_IN_ITERATION = 1000

    def __init__(self, db: Db, provider: DataProvider, results_filename: str):
        self.provider = provider
        self.results_filename = results_filename
        self.db = db
        
        self.testing_points = [1e3, 1e4, 1e5, 1e6]
        self.num_of_elements = 0
        self.crud_measurements = {
            "create": {},
            "read": {},
            "update": {},
            "delete": {}
        }

    def __save_results(self):
        Path("./results").mkdir(parents=True, exist_ok=True)
        
        with open("./results/" + self.results_filename, "w") as outfile: 
            json.dump(self.crud_measurements, outfile, indent = 2)

    def __are_all_points_tested(self) -> bool:
        return len(self.testing_points) == 0

    def __add_rows_to_db(self):
        self.num_of_elements += Test.NUM_OF_ROWS_IN_ITERATION
        cars = self.provider.fetch_rows(Test.NUM_OF_ROWS_IN_ITERATION)
        self.db.insert_elements(cars)

    def __save_measurements(self, create_time, read_time, update_time, delete_time):
        current_testing_points = int(self.testing_points.pop(0))
        self.crud_measurements["create"][current_testing_points] = create_time
        self.crud_measurements["read"][current_testing_points] = read_time
        self.crud_measurements["update"][current_testing_points] = update_time
        self.crud_measurements["delete"][current_testing_points] = delete_time

    def __measure_crud(self):
        car = self.provider.fetch_rows(1)[0]
        record_id = str(car.get_db_record()["id"])
        new_record_car_name = "test"
        self.db.prepare_insert(car)
        
        create_time = self.__measure_operation(lambda: self.db.insert_element(car))
        read_time = self.__measure_operation(lambda: self.db.select_element(record_id))
        update_time = self.__measure_operation(lambda: self.db.update_element(record_id, new_record_car_name))
        delete_time = self.__measure_operation(lambda: self.db.delete_element(record_id))

        self.__save_measurements(create_time, read_time, update_time, delete_time)

    def __measure_operation(self, operation):
        timer = Timer()
        timer.start()
        operation()
        timer.stop()
        return timer.get_elapsed_time()

    def run(self):
        while not self.__are_all_points_tested():
            self.__add_rows_to_db()
            if self.num_of_elements == self.testing_points[0]:
                self.__measure_crud()
                
        self.__save_results()

