import torch 
import glob
import pandas as pd
import numpy as np
import h5py
import re

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

def ReadCurrentAndField(foldername, filepattern,filenum):

    #Read Current
    CurrentData = pd.read_table('./Data/SampleCurrent.txt',skiprows=0,sep='\\s+',index_col=None,header=None) 
    #print(CurrentData)

    fileList = glob.glob(foldername+filepattern)
    fileList=sorted(fileList, key=natural_sort_key)

    #print(CurrentData)
    for i in range(filenum):
        if i == 0:
            print(fileList[i])
            data_temp = ReadData(filename=fileList[i])
            current=CurrentData.loc[i]
            matrix = np.tile(current, (data_temp.shape[0], 1))
            data_temp = np.hstack((matrix,data_temp))
            [row, col] = data_temp.shape
            data = torch.empty(filenum,row,col)
            data[i] = torch.tensor(data_temp)
        else:
            print(fileList[i])
            data_temp = ReadData(filename=fileList[i])
            current=CurrentData.loc[i]
            matrix = np.tile(current, (data_temp.shape[0], 1))
            data_temp = np.hstack((matrix,data_temp))
            data[i] = torch.tensor(data_temp)
    
    return data



def natural_sort_key(s):
    """
    按文件名中的自然数排序
    """
    # 将字符串按照数字和非数字部分分割，返回分割后的子串列表
    sub_strings = re.split(r'(\d+)', s)
    # 如果当前子串由数字组成，则将它转换为整数；否则将其替换成空字符串
    sub_strings = [int(c) if c.isdigit() else '' for c in sub_strings]
    # 返回子串列表
    return sub_strings
            
def ReadCurrentAndField_CNN(foldername, filepattern, filenum):

    #Read Current
    Current = pd.read_table('./Data/SampleCurrent.txt',skiprows=0,sep='\\s+',index_col=None,header=None) 
    # print(Current)
    fileList = glob.glob(foldername+filepattern)
    # fileList = sorted(fileList,key = fileList)
    fileList=sorted(fileList, key=natural_sort_key)
    fileCounter = len(fileList)
    
    for i in range(filenum):
        if i == 0:
            #read position + field data
            data_temp = ReadData(filename=fileList[i])
            my_tensor = torch.t(data_temp)
            y=my_tensor.reshape(6,21,21,21) 
            data = torch.empty(filenum,6,21,21,21)
            data[i] = y
        else:
            data_temp = ReadData(filename=fileList[i])
            my_tensor = torch.t(data_temp)
            y=my_tensor.reshape(6,21,21,21) 
            data[i] = y
        
    Current =  np.array(Current)[0:filenum,:]
    
    return torch.tensor(Current),data

def ReadETHFolder(foldername, filenum, data_shape):

    f_num = 0
    data = np.zeros((filenum, *data_shape))

    for i in range(filenum):

        filename = foldername + str(f_num).zfill(4) + ".h5"
        with h5py.File(filename, "r") as f:
            # get first object name/key; may or may NOT be a group
            a_group_key = list(f.keys())[0]


            # If a_group_key is a dataset name, 
            # this gets the dataset values and returns as a list
            data[i] = np.array(f[a_group_key])
        f_num += 1



        f_num += 1

    return data

def ReadETHFile(filename):



    with h5py.File(filename, "r") as f:
        # get first object name/key; may or may NOT be a group
        a_group_key = list(f.keys())[0]


        # If a_group_key is a dataset name, 
        # this gets the dataset values and returns as a list
        data = np.array(f[a_group_key])

    return data

def add_gaussian_noise(tensor, noise=0.05):
    mean = tensor.mean()
    std = tensor.std()
    noise = torch.randn(tensor.size()) * std * noise + mean
    noisy_tensor = tensor + noise
    return noisy_tensor