import pandas as pd 
import numpy as np
from modules.db.model.car import Car


class DataProvider:
    def __init__(self,path_to_file):
        data_frame = pd.read_csv(filepath_or_buffer=path_to_file,
                         delimiter=";",
                         index_col= None)
        self.data_frame = data_frame[["Car Full Name","Movie Title"]]
        self.start_ind = 0

    def fetch_rows(self,amount):
        end_ind = self.start_ind + amount

        if self.start_ind == self.data_frame.shape[0]:
            return np.array([],dtype=Car)

        if end_ind > self.data_frame.shape[0]:
            end_ind = self.data_frame.shape[0]
            amount = self.data_frame.shape[0] - self.start_ind

        dt_list = np.empty(shape = amount,dtype=Car)
        d_slice = self.data_frame.iloc[self.start_ind:end_ind,:]
        n = 0
        for _, row in d_slice.iterrows():
            sample = Car(full_name = row["Car Full Name"], movie_title = row["Movie Title"])
            dt_list[n] = sample
            n+=1

        self.start_ind = end_ind
        return dt_list
