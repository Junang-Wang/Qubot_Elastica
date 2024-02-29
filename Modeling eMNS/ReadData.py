import torch 
import glob
import pandas as pd
import numpy as np
dataFile = 'Modeling eMNS/Data/MagneticField0.txt'
def ReadData(filename):
    data = torch.tensor(pd.read_table(filename, sep='\\s+', skiprows=1).values)
    return data 

def ReadFolder(foldername, filepattern):
    fileList = glob.glob(foldername+filepattern)
    fileCounter = len(fileList)
    for i in range(fileCounter):
        if i == 0:
            data_temp = ReadData(filename=fileList[i])
            [row, col] = data_temp.shape
            print(row)
            print(col)
            data = torch.empty(fileCounter,row,col)
            data[i] = data_temp
        else:
            data[i] = ReadData(filename=fileList[i])
    
    return data



def ReadCurrentAndField(foldername, filepattern):

    #Read Current
    CurrentData = pd.read_table('Data\SampleCurrent.txt',skiprows=0,sep='\\s+',index_col=None,header=None) 
    #print(CurrentData)

    fileList = glob.glob(foldername+filepattern)
    fileCounter = len(fileList)

    train_file_num = 50
    #print(CurrentData)
    for i in range(fileCounter):
        if i == 0:
            data_temp = ReadData(filename=fileList[i])
            current=CurrentData.loc[i]
            matrix = np.tile(current, (data_temp.shape[0], 1))
            data_temp = np.hstack((matrix,data_temp))
            [row, col] = data_temp.shape
            data = torch.empty(fileCounter,row,col)
            data[i] = torch.tensor(data_temp)
        else:
            data_temp = ReadData(filename=fileList[i])
            current=CurrentData.loc[i]
            matrix = np.tile(current, (data_temp.shape[0], 1))
            data_temp = np.hstack((matrix,data_temp))
            data[i] = torch.tensor(data_temp)
    
    return data
            


def ReadCurrentAndField_CNN(foldername, filepattern):

    #Read Current
    Current = pd.read_table('Data\SampleCurrent.txt',skiprows=0,sep='\\s+',index_col=None,header=None) 
    fileList = glob.glob(foldername+filepattern)
    fileCounter = len(fileList)
    for i in range(fileCounter):
        if i == 0:
            #read position + field data
            data_temp = ReadData(filename=fileList[i])
            my_tensor = torch.t(data_temp)
            y=my_tensor.reshape(6,21,21,21) 
            data = torch.empty(fileCounter,6,21,21,21)
            data[i] = y
        else:
            data_temp = ReadData(filename=fileList[i])
            my_tensor = torch.t(data_temp)
            y=my_tensor.reshape(6,21,21,21) 
            data[i] = y
    
    return torch.tensor(Current.values),data