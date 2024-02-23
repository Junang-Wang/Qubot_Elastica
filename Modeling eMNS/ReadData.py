import torch 
import numpy as np
import pandas as pd
dataFile = 'Modeling eMNS/Data/MagneticField0.txt'
def ReadData(filename):
    data = torch.tensor(pd.read_table(filename, sep='\s+', skiprows=2).values)
    return data 
