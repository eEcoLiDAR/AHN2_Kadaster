#!/usr/bin/env python

import numpy as np
import pandas as pd

np_data = np.load('./Tile02O_intersections.npy')
pd_df = pd.read_pickle("./Tile02O_intersections.pkl")

print(np_data)

print(pd_df.describe())
print(pd_df.head())