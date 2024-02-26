import torch 
import glob
import pandas as pd
dataFile = 'Modeling eMNS/Data/MagneticField0.txt'
def ReadData(filename):
    data = torch.tensor(pd.read_table(filename, sep='\s+', skiprows=2).values)
    return data 

def ReadFolder(foldername, filepattern):
    fileList = glob.glob(foldername+filepattern)
    fileCounter = len(fileList)
    
    for i in range(fileCounter):
        if i == 0:
            data_temp = ReadData(filename=fileList[i])
            [row, col] = data_temp.shape
            data = torch.empty(fileCounter,row,col)
            data[i] = data_temp
        else:
            data[i] = ReadData(filename=fileList[i])
    
    return data

        
            


