from abc import ABC, abstractmethod
from typing import List
from .model.car import Car


class Db(ABC):

    @abstractmethod
    def insert_element(self, car: Car) -> str:
        pass


    @abstractmethod
    def insert_elements(self, cars: List[Car]) -> str:
        pass

    @abstractmethod
    def update_element(self, uid: str, new_full_name: str):
        pass

    @abstractmethod
    def delete_element(self, uid: str):
        pass
