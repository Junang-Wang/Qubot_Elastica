# This file contents neural network codes
import torch
import torch.nn as nn
import torch.nn.functional as F
# set up dataset class
class eMNS_Dataset(torch.utils.data.Dataset):
    def __init__(self,train_x,train_y):
        #data loading
        self.x = train_x 
        self.y = train_y 
        self.n_samples = self.x.shape[0]

    
    def __getitem__(self,index):
        return self.x[index], self.y[index]
    
    def __len__(self):
        return self.n_samples

###############################################################################
# plain 1D Conv network block
###############################################################################
class Plain_CNN_block_1D(nn.Module):
    def __init__(self,in_channel,med_channel):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channel,med_channel,3,padding=1,bias=True)
        #self.BatchNorm = nn.BatchNorm2d(med_channel)
        #self.MaxPool = nn.MaxPool2d(2,2)
        self.relu = nn.ReLU()
        nn.init.kaiming_normal_(self.conv1.weight)
        nn.init.zeros_(self.conv1.bias)
    def forward(self,x):
        #h1 = F.relu(self.BatchNorm(self.conv1(x)))
        #h2 = self.MaxPool(h1)
        h1 = self.relu(self.conv1(x))
        #h2 = self.MaxPool(h1)
        return h1
###############################################################################
# plain Conv network block
###############################################################################
class Plain_CNN_block(nn.Module):
    def __init__(self,in_channel,med_channel):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channel,med_channel,3,padding=1,bias=True)
        #self.BatchNorm = nn.BatchNorm2d(med_channel)
        #self.MaxPool = nn.MaxPool2d(2,2)
        self.relu = nn.ReLU()
        nn.init.kaiming_normal_(self.conv1.weight)
        nn.init.zeros_(self.conv1.bias)
    def forward(self,x):
        #h1 = F.relu(self.BatchNorm(self.conv1(x)))
        #h2 = self.MaxPool(h1)
        h1 = self.relu(self.conv1(x))
        #h2 = self.MaxPool(h1)
        return h1   
    
###############################################################################
# ResNet block
###############################################################################
class ResidualBottleneckBlock_2d(nn.Module):
    def __init__(self,Cin,Cout):
        super().__init__()

        self.block = nn.Sequential(
            nn.BatchNorm2d(Cin),
            nn.ReLU(),
            nn.Conv2d(Cin,Cout//4,1),
            nn.BatchNorm1d(Cout//4),
            nn.ReLU(),
            nn.Conv2d(Cout//4,Cout//4,3,padding=1),
            nn.BatchNorm2d(Cout//4),
            nn.ReLU(),
            nn.Conv1d(Cout//4,Cout,1)
        )
        if Cin == Cout:
            self.shortcut = nn.Identity()
        else:
            self.shortcut = nn.Conv2d(Cin,Cout,1)
    
    def forward(self,x):
        return self.block(x) + self.shortcut(x)

class ResidualBasicBlock_2d(nn.Module):
    def __init__(self,Cin,Cout):
        super().__init__()

        self.block = nn.Sequential(
            nn.BatchNorm2d(Cin),
            nn.ReLU(),
            nn.Conv2d(Cin,Cout,3,padding=1,bias=True),
            nn.BatchNorm2d(Cout),
            nn.ReLU(),
            nn.Conv2d(Cout,Cout,3,padding=1,bias=True)
        )
        if Cin == Cout:
            self.shortcut = nn.Identity()
        else:
            self.shortcut = nn.Conv2d(Cin,Cout,1)
    
    def forward(self,x):
        return self.block(x) + self.shortcut(x)
######################################################################
# fully connected block
######################################################################
class Plain_fc_block(nn.Module):
    def __init__(self,Nin,Nout):
        super().__init__()
        self.fc = nn.Linear(Nin,Nout,bias=True)
        self.relu = nn.ReLU()

        nn.init.kaiming_normal_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)
    def forward(self,x):
        x = torch.flatten(x,start_dim=1)
        scores = self.relu(self.fc(x))
        return scores
#######################################################################
# neural network construction
######################################################################
class NN_stages(nn.Module):
    '''
    Cin: number of input channel
    Cout: number of output channel
    num_block: number of block
    block: type of block used
    '''
    def __init__(self,Cin,Cout,num_block,block):
        super().__init__()
        NNStages = []
        for _ in range(num_block):
            NNStages.append(block(Cin,Cout))
        self.net = nn.Sequential(*NNStages)
    def forward(self,x):
        return self.net(x)

class NN_net(nn.Module):
    '''
    A catchy class to generate simple neural networks by import 
    Conv_args = [(Cin,Cout,num_block),(Cin,Cout,num_block),...]
    fc_args = [(Nin,Nout,num_block),(Nin,Nout,num_block),...]
    Conv_block: custom designed CNN block
    fc_block: custom designed fc block
    '''
    def __init__(self,Conv_args,fc_args,Conv_block,fc_block,num_output):
        super().__init__()
        NNstages = []
        if Conv_args: # if Conv_args is not empty
            for Cin, Cout, num_block in Conv_args:
                NNstages.append(NN_stages(Cin,Cout,num_block,Conv_block))
        if fc_args:
            for Nin, Nout, num_block in fc_args:
                NNstages.append(NN_stages(Nin,Nout,num_block,fc_block))
        self.total_net = nn.Sequential(
            *NNstages,
            nn.Linear(fc_args[-1][1],num_output,bias=True)
            )
    def forward(self,x):
        return  self.total_net(x)
        
class Two_Branches_NN_net(nn.Module):
    '''
    A catchy class to generate simple neural networks by import 
    Conv_args = [(Cin,Cout,num_block),(Cin,Cout,num_block),...]
    fc_args = [(Nin,Nout,num_block),(Nin,Nout,num_block),...]
    Conv_block: custom designed CNN block
    fc_block: custom designed fc block
    '''
    def __init__(self,Conv_args,fc_args,Conv_block,fc_block,num_output):
        super().__init__()
        Conv_stages = []
        Fc_stages = []
        if Conv_args: # if Conv_args is not empty
            for Cin, Cout, num_block in Conv_args:
                Conv_stages.append(NN_stages(Cin,Cout,num_block,Conv_block))
        self.Conv_net = nn.Sequential(*Conv_stages)
        if fc_args:
            for Nin, Nout, num_block in fc_args:
                Fc_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
        self.fc_net_1 = nn.Sequential(*Fc_stages)
        self.fc_net_2 = nn.Sequential(*Fc_stages)
        self.stem_1 = nn.Linear(fc_args[-1][1],num_output,bias=True)
        self.stem_2 = nn.Linear(fc_args[-1][1],num_output,bias=True)
    def forward(self,x):
      h1 = self.Conv_net(x)
      h2 = self.fc_net_1(h1) 
      h3 = self.fc_net_2(h1)
      return  torch.cat((self.stem_1(h2),self.stem_2(h3)),dim=1)

class Two_Branches_Entangled_Late_NN_net(nn.Module):
    '''
    A catchy class to generate simple neural networks by import 
    Conv_args = [(Cin,Cout,num_block),(Cin,Cout,num_block),...]
    fc_args = [(Nin,Nout,num_block),(Nin,Nout,num_block),...]
    Conv_block: custom designed CNN block
    fc_block: custom designed fc block
    '''
    def __init__(self,Conv_args,fc_args,Conv_block,fc_block,num_output):
        super().__init__()
        Conv_stages = []
        Fc_stages = []
        if Conv_args: # if Conv_args is not empty
            for Cin, Cout, num_block in Conv_args:
                Conv_stages.append(NN_stages(Cin,Cout,num_block,Conv_block))

        if fc_args:
            for index, (Nin, Nout, num_block) in enumerate(fc_args):
              if index == 0:
                Conv_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
              else:
                Fc_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
        self.Conv_net = nn.Sequential(*Conv_stages)
        self.fc_net_1 = nn.Sequential(*Fc_stages)
        self.fc_net_2 = nn.Sequential(*Fc_stages)
        self.stem_2to1 = nn.Linear(fc_args[-1][1],fc_args[1][0],bias=True)
        #self.stem_fto1 = nn.Linear(fc_args[0][1],fc_args[1][0],bias=True)
        self.stem_1 = nn.Linear(fc_args[-1][1],num_output,bias=True)
        self.stem_2 = nn.Linear(fc_args[-1][1],num_output,bias=True)
    def forward(self,x):
      h_features = self.Conv_net(x)
      h2 = self.fc_net_2(h_features) 
      h3 = self.fc_net_1(F.tanh(self.stem_2to1(h2)+h_features))
      #return  torch.cat((self.stem_1(h3),self.stem_2(h2)),dim=1)
      return torch.cat((self.stem_2(h2),self.stem_1(h3)),dim=1)


class Two_Branches_Entangled_Early_NN_net(nn.Module):
    '''
    A catchy class to generate simple neural networks by import 
    Conv_args = [(Cin,Cout,num_block),(Cin,Cout,num_block),...]
    fc_args = [(Nin,Nout,num_block),(Nin,Nout,num_block),...]
    Conv_block: custom designed CNN block
    fc_block: custom designed fc block
    '''
    def __init__(self,Conv_args,fc_args,Conv_block,fc_block,num_output):
        super().__init__()
        Conv_stages = []
        Fc_stages = []
        if Conv_args: # if Conv_args is not empty
            for Cin, Cout, num_block in Conv_args:
                Conv_stages.append(NN_stages(Cin,Cout,num_block,Conv_block))

        if fc_args:
            for index, (Nin, Nout, num_block) in enumerate(fc_args):
              if index == 0:
                Conv_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
              else:
                Fc_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
        self.Conv_net = nn.Sequential(*Conv_stages)
        self.fc_net_1 = nn.Sequential(*Fc_stages)
        self.fc_net_2_0 = nn.Sequential(*Fc_stages[:1])
        self.fc_net_2 = nn.Sequential(*Fc_stages[1:])
        self.stem_2to1 = nn.Linear(fc_args[1][1],fc_args[-1][1],bias=True)
        self.stem_1 = nn.Linear(fc_args[-1][1],num_output,bias=True)
        self.stem_2 = nn.Linear(fc_args[-1][1],num_output,bias=True)
    def forward(self,x):
      h_features = self.Conv_net(x)
      h1 = self.fc_net_1(h_features)
      h2_0= self.fc_net_2_0(h_features) #the first hidden layer after features
      h2to1 = self.stem_2to1(h2_0) #convert h2_0 to h1 
      h2 = self.fc_net_2(h2_0)
      #return  torch.cat((self.stem_1(F.tanh(h2to1+h1) ),self.stem_2(h2) ),dim=1)
      return  torch.cat((self.stem_2(h2),(self.stem_1(F.tanh(h2to1+h1)) ) ),dim=1)

class Two_Branches_Fully_Entangled_Early_NN_net(nn.Module):
    '''
    A catchy class to generate simple neural networks by import 
    Conv_args = [(Cin,Cout,num_block),(Cin,Cout,num_block),...]
    fc_args = [(Nin,Nout,num_block),(Nin,Nout,num_block),...]
    Conv_block: custom designed CNN block
    fc_block: custom designed fc block
    '''
    def __init__(self,Conv_args,fc_args,Conv_block,fc_block,num_output):
        super().__init__()
        Conv_stages = []
        Fc_stages = []
        if Conv_args: # if Conv_args is not empty
            for Cin, Cout, num_block in Conv_args:
                Conv_stages.append(NN_stages(Cin,Cout,num_block,Conv_block))

        if fc_args:
            for index, (Nin, Nout, num_block) in enumerate(fc_args):
              if index == 0:
                Conv_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
              else:
                Fc_stages.append(NN_stages(Nin,Nout,num_block,fc_block))
        self.Conv_net = nn.Sequential(*Conv_stages)
        self.fc_net_1_0 = nn.Sequential(*Fc_stages[:1])
        self.fc_net_1 = nn.Sequential(*Fc_stages[1:])
        self.fc_net_2_0 = nn.Sequential(*Fc_stages[:1])
        self.fc_net_2 = nn.Sequential(*Fc_stages[1:])
        self.stem_2to1 = nn.Linear(fc_args[1][1],fc_args[-1][1],bias=True)
        self.stem_1to2 = nn.Linear(fc_args[1][1],fc_args[-1][1],bias=True)
        self.stem_1 = nn.Linear(fc_args[-1][1],num_output,bias=True)
        self.stem_2 = nn.Linear(fc_args[-1][1],num_output,bias=True)
    def forward(self,x):
      h_features = self.Conv_net(x)
      h1_0 = self.fc_net_1_0(h_features)
      h2_0= self.fc_net_2_0(h_features) #the first hidden layer after features

      h1to2 = self.stem_2to1(h1_0) #convert h1_0 to h2
      h2to1 = self.stem_2to1(h2_0) #convert h2_0 to h1

      h1 = self.fc_net_2(h1_0)
      h2 = self.fc_net_2(h2_0)
      return  torch.cat((self.stem_1(F.tanh(h2to1+h1) ),self.stem_2(F.tanh(h1to2+h2)) ),dim=1)

################################################################################
# init weigth
################################################################################
@torch.no_grad()
def weight_init(m):
    #print(m)
    #print('Initiating weight and bias...')
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        #torch.nn.init.normal_(m.weight,0,1)
        torch.nn.init.kaiming_normal_(m.weight)
        #torch.nn.init.ones_(m.weight)
        torch.nn.init.zeros_(m.bias)
        #print(m.weight)
    elif type(m) == nn.BatchNorm2d:
        torch.nn.init.normal_(m.weight,1,1)
        #torch.nn.init.kaiming_normal_(m.weight)
        torch.nn.init.zeros_(m.bias)
        #print(m.weight)

@torch.no_grad()
def weight_init_1D(m):
    #print(m)
    #print('Initiating weight and bias...')
    if type(m) == nn.Linear or type(m) == nn.Conv1d:
        #torch.nn.init.normal_(m.weight,0,1)
        torch.nn.init.kaiming_normal_(m.weight)
        #torch.nn.init.ones_(m.weight)
        torch.nn.init.zeros_(m.bias)
        #print(m.weight)
    elif type(m) == nn.BatchNorm1d:
        torch.nn.init.normal_(m.weight,1,1)
        #torch.nn.init.kaiming_normal_(m.weight)
        torch.nn.init.zeros_(m.bias)
        #print(m.weight)