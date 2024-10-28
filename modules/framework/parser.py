import pandas as pd 
import numpy as np
from modules.db.model.car import Car


class Return_Car:
    def __init__(self):
        df = pd.read_csv(filepath_or_buffer="./data/CarsInMovies.csv",
                         delimiter=";",
                         index_col= None)
        self.df = df[["Car Full Name","Movie Title"]]
        self.s_ind = 0
        self.e_ind = 0

    def gimmie_amount(self,amount):
        #start_time = timeit.default_timer()
        self.e_ind+=amount
        if self.s_ind == self.df.shape[0]:
            return np.array([],dtype=Car)

        if self.e_ind > self.df.shape[0]:
            self.e_ind = self.df.shape[0]
            amount = self.df.shape[0] - self.s_ind
        else :
            pass

        print(f"indexes {self.s_ind} : {self.e_ind-1}")
        dt = np.empty(shape = amount,dtype=Car)
        d = self.df.iloc[self.s_ind:self.e_ind,:]
        n = 0
        for index, row in d.iterrows():
            sample = Car(full_name = row["Car Full Name"],movie_title=row["Movie Title"]) 
            dt[n] = sample
            n+=1
        
        self.s_ind = self.e_ind
        #print(f"Time taken : {timeit.default_timer() - start_time:<.1f}s")
        return dt

