#########################################################################
# Training loop
#############################################################################
import torch
import torch.nn.functional as F
from early_stopping import EarlyStopping, EarlyDecay
from utils import compute_discrete_curl, denorm
import numpy as np

def adjust_learning_rate_sch(optimizer, lrd, epoch, schedule):
    """
    Multiply lrd to the learning rate if epoch in schedule

    Return: None, but learning rate (lr) might be updated
    """
    if epoch in schedule:
        for param_group in optimizer.param_groups:
            print(f'lr decay from { param_group["lr"] } to {param_group["lr"]*lrd}')
            param_group['lr'] *= lrd 

def adjust_learning_rate_cosine(optimizer, lr_max, lr_min,max_epoch,tt,len_dataloader):
    """
    Cosine decay to the learning rate every iternation

    Return: None, but learning rate (lr) might be updated
    """

    for param_group in optimizer.param_groups:
        new_lr = lr_min+0.5*(lr_max-lr_min)*(1+np.cos(tt/(max_epoch*len_dataloader)*np.pi))
        # print(f'lr decay from { param_group["lr"] } to {new_lr}')
        param_group['lr'] = new_lr


def adjust_learning_rate(optimizer, lrd):
    """
    Multiply lrd to the learning rate

    Return: None, but learning rate (lr) might be updated
    """
    for param_group in optimizer.param_groups:
      print(f'lr decay from { param_group["lr"] } to {param_group["lr"]*lrd}')
      param_group['lr'] *= lrd

def adjust_learning_rate_linear(optimizer, linear_increment):
    """
    add linear_increment to the learning rate

    Return: None, but learning rate (lr) might be updated
    """
    for param_group in optimizer.param_groups:
      print(f'lr decay from { param_group["lr"] } to {param_group["lr"]+linear_increment}')
      param_group['lr'] += linear_increment

######################################################################################################################################
def train_part(model,optimizer,train_loader,valid_loader, epochs = 1, learning_rate_decay =.1,weight_decay=1e-4, schedule=[], verbose=True, device= 'cuda'):
    """
    Train a model using torch API

    Inputs: 
    - model: A Pytorch Module giving the model to train
    - optimizer: An optimizer object we will use to train the model
    - epochs: A Python integer giving the number of epochs to train for

    Returns: model accuracies, prints model loss during training
    """
    model = model.to(device=device)
    num_iters = epochs*len(train_loader)
    print_every = 100 
    adjust_epoch_count = 0
    if verbose:
        num_prints = num_iters // print_every + 1 
    else:
        num_prints = epochs 
    
    # initial loss history and iter history
    rmse_history = torch.zeros(num_prints,dtype = torch.float)
    rmse_val_history = torch.zeros(num_prints,dtype = torch.float)
    iter_history = torch.zeros(num_prints,dtype = torch.float)
    loss_history = torch.zeros(num_prints,dtype = torch.float)
     

    ###########################################################
    # train loop:
    # step 1: update learning rate
    # step 2: put model to train model, move data to gpu 
    # step 3: compute scores, calculate loss function
    # step 4: Zero out all of gradients for the variables which the optimizer will update
    # step 5: compute gradient of loss, update parameters
    ###########################################################
    for epoch in range(epochs):
      for t, (x,y) in enumerate(train_loader):
        model.train()
        x = x.to(device=device,dtype=torch.float)
        y = y.to(device=device,dtype=torch.float)
        #scores = model(x).reshape(-1)#for one output
        #L1_norm = 0
        #for param in model.parameters():
        #  L1_norm += weight_decay*torch.sum(torch.abs(param))
        #loss = F.mse_loss(scores,y) + L1_norm
        scores = model(x)
        # loss = F.cross_entropy(scores,y)
        # mean squared error
        loss = F.mse_loss(scores, y)
        optimizer.zero_grad() #zero out all of gradient
        loss.backward() # compute gradient of loss
        optimizer.step() #update parameters
        
        tt = t + epoch*len(train_loader) +1

###########################################################
# print loss during training 
        if verbose and (tt % print_every == 1 or (epoch == epochs -1 and t == len(train_loader) -1) ) :
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val = check_rmse(valid_loader,model,device)
          rmse = check_rmse(train_loader,model, device)
          rmse_val_history[tt//print_every] = rmse_val
          rmse_history[tt // print_every] = rmse 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (rmse_val >= 0.995) and (epoch > 10):
        #     print('rmse_val larger than 0.995, end the training loop')
        #     return rmse_history, rmse_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val = check_rmse(valid_loader,model, device)
          rmse = check_rmse(train_loader,model, device)
          rmse_val_history[epoch] = rmse_val
          rmse_history[epoch] = rmse 
          iter_history[epoch] = tt 
          loss_history[epoch] = loss.item()
          print()
          adjust_epoch_count += 1
          # if epoch > 6 and adjust_epoch_count > 3:
          #   if loss_history[epoch-3:epoch+1].mean() >= 0.90*loss_history[epoch-7:epoch-3].mean():
          #     adjust_learning_rate(optimizer=optimizer,lrd= learning_rate_decay)
          #     print(f'{loss_history[epoch-3:epoch+1].mean():.2f} >= {0.95*loss_history[epoch-7:epoch-3].mean():.2f}')
              # adjust learning rate if loss has not decrease in 3 epochs
              # adjust_epoch_count = 0
        #   if epoch > 10:    
        #     if (rmse_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
        #       print('rmse_val reachs to 100%, end the training loop')
              # return rmse_history, rmse_val_history,loss_history, iter_history
          
    return rmse_history, rmse_val_history,loss_history, iter_history



######################################################################################################################################
def train_part_v1(model,optimizer,train_loader,valid_loader, epochs = 1, learning_rate_decay =.1,weight_decay=1e-4, schedule=[], verbose=True, device= 'cuda'):
    """
    Train a model using torch API

    Inputs: 
    - model: A Pytorch Module giving the model to train
    - optimizer: An optimizer object we will use to train the model
    - epochs: A Python integer giving the number of epochs to train for

    Returns: model accuracies, prints model loss during training
    """
    model = model.to(device=device)
    num_iters = epochs*len(train_loader)
    print_every = 100 
    adjust_epoch_count = 0
    if verbose:
        num_prints = num_iters // print_every + 1 
    else:
        num_prints = epochs 
    
    # initial loss history and iter history
    rmse_history = torch.zeros(num_prints,dtype = torch.float)
    rmse_val_history = torch.zeros(num_prints,dtype = torch.float)
    iter_history = torch.zeros(num_prints,dtype = torch.float)
    loss_history = torch.zeros(num_prints,dtype = torch.float)
    loss_val_history= torch.zeros(num_prints,dtype = torch.float)


    patience = 5	# 当验证集损失在连5次训练周期中都没有得到降低时，停止模型训练，以防止模型过拟合
    early_stopping = EarlyStopping(patience, verbose=True)     
    epoch_stop = 0

    ###########################################################
    # train loop:
    # step 1: update learning rate
    # step 2: put model to train model, move data to gpu 
    # step 3: compute scores, calculate loss function
    # step 4: Zero out all of gradients for the variables which the optimizer will update
    # step 5: compute gradient of loss, update parameters
    ###########################################################
    for epoch in range(epochs):
      for t, (x,y) in enumerate(train_loader):
        model.train()
        x = x.to(device=device,dtype=torch.float)
        y = y.to(device=device,dtype=torch.float)
        #scores = model(x).reshape(-1)#for one output
        #L1_norm = 0
        #for param in model.parameters():
        #  L1_norm += weight_decay*torch.sum(torch.abs(param))
        #loss = F.mse_loss(scores,y) + L1_norm
        scores = model(x)
        # loss = F.cross_entropy(scores,y)
        # mean squared error
        loss = F.mse_loss(scores, y)
        optimizer.zero_grad() #zero out all of gradient
        loss.backward() # compute gradient of loss
        optimizer.step() #update parameters
        
        tt = t + epoch*len(train_loader) +1

        ###########################################################
        # print loss during training 
        if verbose and (tt % print_every == 1 or (epoch == epochs -1 and t == len(train_loader) -1) ) :
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val = check_rmse(valid_loader,model,device)
          rmse = check_rmse(train_loader,model, device)
          rmse_val_history[tt//print_every] = rmse_val
          rmse_history[tt // print_every] = rmse 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (rmse_val >= 0.995) and (epoch > 10):
        #     print('rmse_val larger than 0.995, end the training loop')
        #     return rmse_history, rmse_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val,loss_val= check_rmse(valid_loader,model, device)
          rmse,loss_train = check_rmse(train_loader,model, device)
          rmse_val_history[epoch] = rmse_val
          rmse_history[epoch] = rmse 
          iter_history[epoch] = tt 
          loss_history[epoch] = loss.item()
          loss_val_history[epoch] = loss_val

          print()
          adjust_epoch_count += 1
          # if epoch > 6 and adjust_epoch_count > 3:
          #   if loss_history[epoch-3:epoch+1].mean() >= 0.90*loss_history[epoch-7:epoch-3].mean():
          #     adjust_learning_rate(optimizer=optimizer,lrd= learning_rate_decay)
          #     print(f'{loss_history[epoch-3:epoch+1].mean():.2f} >= {0.95*loss_history[epoch-7:epoch-3].mean():.2f}')
              # adjust learning rate if loss has not decrease in 3 epochs
              # adjust_epoch_count = 0
        #   if epoch > 10:    
        #     if (rmse_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
        #       print('rmse_val reachs to 100%, end the training loop')
              # return rmse_history, rmse_val_history,loss_history, iter_history
      #set early stop
      early_stopping(loss_history[epoch], model)
    	# 若满足 early stopping 要求
      if early_stopping.early_stop:
        epoch_stop = epoch
        print("Early stopping")
		    #结束模型训练
        break

          
    return rmse_history, rmse_val_history,loss_history, iter_history, loss_val_history,epoch_stop

######################################################################################################################################
def train_part_GM(model,optimizer,train_loader,valid_loader, epochs = 1, learning_rate_decay =.1,weight_decay=1e-4, schedule=[], grid_space= 20*20*20, DF= False, verbose=True, device= 'cuda',maxB=[],minB=[], lr_max=1e-4, lr_min=2.5e-6,max_epoch=200, linear_lr=False):
    """
    Train a model using torch API

    Inputs: 
    - model: A Pytorch Module giving the model to train
    - optimizer: An optimizer object we will use to train the model
    - epochs: A Python integer giving the number of epochs to train for

    Returns: model accuracies, prints model loss during training
    """
    model = model.to(device=device)
    num_iters = epochs*len(train_loader)
    print_every = 100 
    adjust_epoch_count = 0
    if verbose:
        num_prints = num_iters // print_every + 1 
    else:
        num_prints = epochs 
    
    # initial loss history and iter history
    rmse_history = torch.zeros(num_prints,dtype = torch.float)
    rmse_val_history = torch.zeros(num_prints,dtype = torch.float)
    iter_history = torch.zeros(num_prints,dtype = torch.float)
    loss_history = torch.zeros(num_prints,dtype = torch.float)
    mse_history= torch.zeros(num_prints,dtype = torch.float)
    mse_val_history= torch.zeros(num_prints,dtype = torch.float)

    patience = 20	# 当验证集损失在连5次训练周期中都没有得到降低时，停止模型训练，以防止模型过拟合
    early_stopping = EarlyStopping(patience, verbose=True)     
    early_decay = EarlyDecay(patience, delta=0.005, lr_min=lr_min)
    epoch_stop = 0

    ###########################################################
    # train loop:
    # step 1: update learning rate
    # step 2: put model to train model, move data to gpu 
    # step 3: compute scores, calculate loss function
    # step 4: Zero out all of gradients for the variables which the optimizer will update
    # step 5: compute gradient of loss, update parameters
    ###########################################################
    for epoch in range(epochs):
      for t, (x,y) in enumerate(train_loader):
        model.train()
        x = x.to(device=device,dtype=torch.float)
        y = y.to(device=device,dtype=torch.float)

        if DF: 
          preds = compute_discrete_curl(model(x),device=device)
        else:
          preds = model(x)
        # loss function in the paper "Modeling Electromagnetic Navigation Systems" 
        # loss= lamda_b*|y-preds| + lamda_g*| nabla(y) - nabla(preds)|
        loss = F.l1_loss(preds, y) + grad_loss_Jacobain(preds,y)
        optimizer.zero_grad() #zero out all of gradient
        loss.backward() # compute gradient of loss
        optimizer.step() #update parameters
        
        tt = t + epoch*len(train_loader) +1
        adjust_learning_rate_cosine(optimizer, lr_max, lr_min,max_epoch,tt,len(train_loader))
        # early_decay(loss, optimizer, learning_rate_decay)
        ###########################################################
        # print loss during training 
        if verbose and (tt % print_every == 1 or (epoch == epochs -1 and t == len(train_loader) -1) ) :
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val,mse_val,Rsquare = check_rmse_CNN(valid_loader,model,grid_space, device, DF,maxB=maxB,minB=minB)
          rmse,mse_train,R_TEMP = check_rmse_CNN(train_loader,model, grid_space, device, DF,maxB=maxB,minB=minB)
          rmse_val_history[tt//print_every] = rmse_val
          rmse_history[tt // print_every] = rmse 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (rmse_val >= 0.995) and (epoch > 10):
        #     print('rmse_val larger than 0.995, end the training loop')
        #     return rmse_history, rmse_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          rmse_val,mse_val,Rsquare= check_rmse_CNN(valid_loader,model, grid_space, device,DF,maxB=maxB,minB=minB)
          rmse,mse_train,R_TEMP = check_rmse_CNN(train_loader,model, grid_space, device,DF,maxB=maxB,minB=minB)
          rmse_val_history[epoch] = rmse_val
          rmse_history[epoch] = rmse 
          iter_history[epoch] = tt 
          loss_history[epoch] = loss.item()
          mse_history[epoch] = mse_train
          mse_val_history[epoch] = mse_val

          print()
          adjust_epoch_count += 1
      if linear_lr:
        adjust_learning_rate_linear(optimizer, linear_increment=1e-6)
      else:
        adjust_learning_rate_sch(optimizer, learning_rate_decay, epoch, schedule)
      epoch_stop = epoch

    

    return rmse_history, rmse_val_history,loss_history, iter_history,mse_history, mse_val_history,epoch_stop,Rsquare

# TODO update Root mean squared error
def check_rmse(dataloader,model,device,verbose=False):
    num_samples = 0
    mse = 0
    model.eval() # set model to evaluation model 
    if not verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device,dtype=torch.float)
          y = y.to(device=device,dtype=torch.float)
          num_samples += x.shape[0]
          scores = model(x)
          # preds = torch.argmax(scores,dim=1)
          # num_correct += (preds == y).sum()
          mse += F.mse_loss(scores, y, reduction='sum')
        #   num_samples += preds.size(0)
        # acc = float(num_correct) / num_samples 
        rmse = torch.sqrt(mse/num_samples)
        print(f'Got rmse {rmse}')

    if verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device)
          y = y.to(device=device)
          scores = model(x)
          
           
    return rmse , mse/len(dataloader)

def get_mean_of_dataloader(dataloader,model,device):
    num_samples = 0
    b = torch.zeros(1,device=device)
    model.eval()
    for x,y in dataloader:
        y = y.to(device=device,dtype=torch.float)
        # use sum instead of mean, what do you think?
        y_sum = y.sum(dim=0,keepdim=True)
        num_samples += y.shape[0]
        # print(y.shape[0])
        b =b+y_sum
    return b/num_samples


def check_rmse_CNN(dataloader,model, grid_space, device, DF, verbose=False, maxB=[],minB=[]):
    '''
    Check RMSE of CNN
    '''
    mse_temp = 0
    R_temp=0
    Rsquare=0
    num_samples = 0
    # print(Bfield_mean)

    data = next(iter(dataloader))
    mean = data[0].mean()

    Bfield_mean=get_mean_of_dataloader(dataloader,model,device)

    model.eval() # set model to evaluation model 
    if not verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device,dtype=torch.float)
          y = y.to(device=device,dtype=torch.float)
          num_samples += x.shape[0]
          if DF:
            scores = compute_discrete_curl(model(x))
          else:
            scores = model(x)
          
          # compute mse and R2 by de-normalize data
          mse_temp += F.mse_loss(1e3*denorm(scores,maxB,minB), 1e3*denorm(y,maxB,minB) ,reduction='sum')
          R_temp += F.mse_loss(1e3*denorm(Bfield_mean.expand_as(y),maxB,minB), 1e3*denorm(y,maxB,minB), reduction='sum')


        rmse = torch.sqrt(mse_temp/num_samples/grid_space/3)

        Rsquare=1-mse_temp/R_temp/num_samples
        print(f'Got rmse {rmse}')

        
    #####################################################
    if verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device)
          y = y.to(device=device)
          scores = model(x)
          #preds = (torch.round(scores)).reshape(-1)
          preds = torch.argmax(scores,dim=1)
           
    return rmse, mse_temp/num_samples/grid_space,Rsquare


def grad_loss(preds, y):
   '''
   preds, y shape: (batch, dimension, grid_x, grid_y, grid_z)
   This function computes lamda_g*| nabla(y) - nabla(preds)|
   '''
   grad_preds = torch.gradient(preds,spacing=1.0)
   grad_y = torch.gradient(y, spacing=1)
   grad_loss = 0
   for i in range(2,5):
      # accumulate grad loss for grad_x,y,z
      grad_loss += torch.mean(torch.abs(grad_y[i]-grad_preds[i]))/3
   return grad_loss

def grad_loss_Jacobain(preds,y):
  '''
   preds, y shape: (batch, dimension, grid_x, grid_y, grid_z)
   This function computes lamda_g*| nabla(y) - nabla(preds)| by Jacobian 
   '''
  Jaco_preds,_ = Jacobian3(preds)
  Jaco_y    ,_ = Jacobian3(y)

  grad_loss = torch.mean(torch.abs(Jaco_preds - Jaco_y))

  return grad_loss


def Jacobian3(x):
  '''
  Jacobian for 3D vector field
  -------input----------
  x shape: (batch, dimension,grid_x, grid_y, grid_z)
  '''

  dudx = x[:, 0, 1:, :, :] - x[:, 0, :-1, :, :]
  dvdx = x[:, 1, 1:, :, :] - x[:, 1, :-1, :, :]
  dwdx = x[:, 2, 1:, :, :] - x[:, 2, :-1, :, :]
  
  dudy = x[:, 0, :, 1:, :] - x[:, 0, :, :-1, :]
  dvdy = x[:, 1, :, 1:, :] - x[:, 1, :, :-1, :]
  dwdy = x[:, 2, :, 1:, :] - x[:, 2, :, :-1, :]

  dudz = x[:, 0, :, :, 1:] - x[:, 0, :, :, :-1]
  dvdz = x[:, 1, :, :, 1:] - x[:, 1, :, :, :-1]
  dwdz = x[:, 2, :, :, 1:] - x[:, 2, :, :, :-1]

  dudx = torch.cat((dudx, torch.unsqueeze(dudx[:,-1],dim=1)), dim=1)
  dvdx = torch.cat((dvdx, torch.unsqueeze(dvdx[:,-1],dim=1)), dim=1)
  dwdx = torch.cat((dwdx, torch.unsqueeze(dwdx[:,-1],dim=1)), dim=1)

  dudy = torch.cat((dudy, torch.unsqueeze(dudy[:,:,-1],dim=2)), dim=2)
  dvdy = torch.cat((dvdy, torch.unsqueeze(dvdy[:,:,-1],dim=2)), dim=2)
  dwdy = torch.cat((dwdy, torch.unsqueeze(dwdy[:,:,-1],dim=2)), dim=2)

  dudz = torch.cat((dudz, torch.unsqueeze(dudz[:,:,:,-1],dim=3)), dim=3)
  dvdz = torch.cat((dvdz, torch.unsqueeze(dvdz[:,:,:,-1],dim=3)), dim=3)
  dwdz = torch.cat((dwdz, torch.unsqueeze(dwdz[:,:,:,-1],dim=3)), dim=3)

  u = dwdy - dvdz
  v = dudz - dwdx
  w = dvdx - dudy

  j = torch.stack([dudx,dudy,dudz,dvdx,dvdy,dvdz,dwdx,dwdy,dwdz],axis=-1)
  c = torch.stack([u,v,w],axis=-1) #vorticity

  return j,c