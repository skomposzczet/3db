import numpy as np
from modules.db.model.car import Car
import os.path
import hashlib
import pandas as pd
from dotenv import load_dotenv
import zipfile
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi


class DataProvider:
    def __init__(self, path_to_file):
        self.start_ind = 0
        self.data_path = path_to_file
        self.hashsum = str(os.getenv("DATEFILE_HASH"))
        self.data_frame = self.__check_instance()

    def __check_instance(self) -> pd.DataFrame:
        check = None
        path_split = self.data_path.split(sep="/")
        path = "/".join(path_split[:2])

        if os.path.isfile(self.data_path):
            print("Data avaible in declared path, testing checksum")
            check = self.__check_md5()
            if check:
                dt = pd.read_csv(filepath_or_buffer=self.data_path,
                                 sep=";",
                                 index_col=0)

        if (not os.path.isfile(self.data_path)) or not check:
            if not os.path.exists(path):
                os.makedirs(path)

            if (not os.path.isfile(self.data_path)):
                print("Data not avaible in declared path, begin downloading")
            if not check:
                print("Checksum failed redownloading")

            dataset = "alexandervarlamov/cars-trucks-bikes-buses-in-movies"
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_file(dataset, 'Cars in Movies.csv', path)
            with zipfile.ZipFile(f"{path}/Cars%20in%20Movies.csv.zip", "r") as zip_ref:
                zip_ref.extractall(f"{path}")

            check = self.__check_md5()
            if check:
                dt = pd.read_csv(filepath_or_buffer=self.data_path,
                                 sep=";",
                                 index_col=0)
            else:
                print("md5 failed")

        data = dt[["Car Full Name",
                   "Movie Title",
                   "Brand",
                   "Movie Type",
                   "Class"]]

        return data

    def __check_md5(self) -> bool:
        # Open,close, read file and calculate MD5 on its contents
        with open(self.data_path, 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()

        # Finally compare original MD5 with freshly calculated
        if self.hashsum == md5_returned:
            print("MD5 verified.")
            return True
        else:
            print("MD5 verification failed!.")
            return False

    def fetch_rows(self, amount) -> list:
        end_ind = self.start_ind + amount

        if self.start_ind == self.data_frame.shape[0]:
            return np.array([], dtype=Car)

        if end_ind > self.data_frame.shape[0]:
            end_ind = self.data_frame.shape[0]
            amount = self.data_frame.shape[0] - self.start_ind

        dt_list = np.empty(shape=amount, dtype=Car)
        d_slice = self.data_frame.iloc[self.start_ind:end_ind, :]
        n = 0
        for _, row in d_slice.iterrows():
            sample = Car(
                full_name=row["Car Full Name"],
                car_brand=row["Brand"],
                car_class=row["Class"],
                movie_title=row["Movie Title"],
                movie_type=row["Movie Type"])
            dt_list[n] = sample
            n += 1

        self.start_ind = end_ind
        return dt_list
