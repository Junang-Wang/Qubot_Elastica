#########################################################################
# Training loop
#############################################################################
import torch
import torch.nn.functional as F
from early_stopping import EarlyStopping
from utils import compute_discrete_curl

def adjust_learning_rate_sch(optimizer, lrd, epoch, schedule):
    """
    Multiply lrd to the learning rate if epoch in schedule

    Return: None, but learning rate (lr) might be updated
    """
    if epoch in schedule:
        for param_group in optimizer.param_groups:
            print(f'lr decay from { param_group["lr"] } to {param_group["lr"]*lrd}')
            param_group['lr'] *= lrd 
def adjust_learning_rate(optimizer, lrd):
    """
    Multiply lrd to the learning rate

    Return: None, but learning rate (lr) might be updated
    """
    for param_group in optimizer.param_groups:
      print(f'lr decay from { param_group["lr"] } to {param_group["lr"]*lrd}')
      param_group['lr'] *= lrd

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
    RMSE_history = torch.zeros(num_prints,dtype = torch.float)
    RMSE_val_history = torch.zeros(num_prints,dtype = torch.float)
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
          RMSE_val = check_RMSE(valid_loader,model,device)
          RMSE = check_RMSE(train_loader,model, device)
          RMSE_val_history[tt//print_every] = RMSE_val
          RMSE_history[tt // print_every] = RMSE 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (RMSE_val >= 0.995) and (epoch > 10):
        #     print('RMSE_val larger than 0.995, end the training loop')
        #     return RMSE_history, RMSE_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          RMSE_val = check_RMSE(valid_loader,model, device)
          RMSE = check_RMSE(train_loader,model, device)
          RMSE_val_history[epoch] = RMSE_val
          RMSE_history[epoch] = RMSE 
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
        #     if (RMSE_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
        #       print('RMSE_val reachs to 100%, end the training loop')
              # return RMSE_history, RMSE_val_history,loss_history, iter_history
          
    return RMSE_history, RMSE_val_history,loss_history, iter_history



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
    RMSE_history = torch.zeros(num_prints,dtype = torch.float)
    RMSE_val_history = torch.zeros(num_prints,dtype = torch.float)
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
          RMSE_val = check_RMSE(valid_loader,model,device)
          RMSE = check_RMSE(train_loader,model, device)
          RMSE_val_history[tt//print_every] = RMSE_val
          RMSE_history[tt // print_every] = RMSE 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (RMSE_val >= 0.995) and (epoch > 10):
        #     print('RMSE_val larger than 0.995, end the training loop')
        #     return RMSE_history, RMSE_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          RMSE_val,loss_val= check_RMSE(valid_loader,model, device)
          RMSE,loss_train = check_RMSE(train_loader,model, device)
          RMSE_val_history[epoch] = RMSE_val
          RMSE_history[epoch] = RMSE 
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
        #     if (RMSE_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
        #       print('RMSE_val reachs to 100%, end the training loop')
              # return RMSE_history, RMSE_val_history,loss_history, iter_history
      #set early stop
      early_stopping(loss_history[epoch], model)
    	# 若满足 early stopping 要求
      if early_stopping.early_stop:
        epoch_stop = epoch
        print("Early stopping")
		    #结束模型训练
        break

          
    return RMSE_history, RMSE_val_history,loss_history, iter_history, loss_val_history,epoch_stop

######################################################################################################################################
def train_part_GM(model,optimizer,train_loader,valid_loader, epochs = 1, learning_rate_decay =.1,weight_decay=1e-4, schedule=[], grid_space= 20*20*20, DF= False, verbose=True, device= 'cuda'):
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
    RMSE_history = torch.zeros(num_prints,dtype = torch.float)
    RMSE_val_history = torch.zeros(num_prints,dtype = torch.float)
    iter_history = torch.zeros(num_prints,dtype = torch.float)
    loss_history = torch.zeros(num_prints,dtype = torch.float)
    loss_val_history= torch.zeros(num_prints,dtype = torch.float)


    patience = 10	# 当验证集损失在连5次训练周期中都没有得到降低时，停止模型训练，以防止模型过拟合
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

        if DF: 
          preds = compute_discrete_curl(model(x))
        else:
          preds = model(x)
        # loss function in the paper "Modeling Electromagnetic Navigation Systems" 
        # loss= lamda_b*|y-preds| + lamda_g*| nabla(y) - nabla(preds)|
        loss = F.l1_loss(preds, y) + grad_loss(preds,y)
        optimizer.zero_grad() #zero out all of gradient
        loss.backward() # compute gradient of loss
        optimizer.step() #update parameters
        
        tt = t + epoch*len(train_loader) +1

        ###########################################################
        # print loss during training 
        if verbose and (tt % print_every == 1 or (epoch == epochs -1 and t == len(train_loader) -1) ) :
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          RMSE_val,loss_val,Rsquare = check_RMSE_CNN(valid_loader,model,grid_space, device)
          RMSE,loss_train,R_TEMP = check_RMSE_CNN(train_loader,model, grid_space, device)
          RMSE_val_history[tt//print_every] = RMSE_val
          RMSE_history[tt // print_every] = RMSE 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = loss.item()
          print()
        #   if (RMSE_val >= 0.995) and (epoch > 10):
        #     print('RMSE_val larger than 0.995, end the training loop')
        #     return RMSE_history, RMSE_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          RMSE_val,loss_val,Rsquare= check_RMSE_CNN(valid_loader,model, grid_space, device)
          RMSE,loss_train,R_TEMP = check_RMSE_CNN(train_loader,model, grid_space, device)
          RMSE_val_history[epoch] = RMSE_val
          RMSE_history[epoch] = RMSE 
          iter_history[epoch] = tt 
          loss_history[epoch] = loss_train
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
        #     if (RMSE_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
        #       print('RMSE_val reachs to 100%, end the training loop')
              # return RMSE_history, RMSE_val_history,loss_history, iter_history
      #set early stop
      early_stopping(loss_history[epoch], model)
    	# 若满足 early stopping 要求
      if early_stopping.early_stop:
        epoch_stop = epoch
        print("Early stopping")
		    #结束模型训练
        break

          
    return RMSE_history, RMSE_val_history,loss_history, iter_history, loss_val_history,epoch_stop,Rsquare

# TODO update Root mean squared error
def check_RMSE(dataloader,model,device,verbose=False):
    num_samples = 0
    MSE = 0
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
          MSE += F.mse_loss(scores, y, reduction='sum')
        #   num_samples += preds.size(0)
        # acc = float(num_correct) / num_samples 
        RMSE = torch.sqrt(MSE/num_samples)
        print(f'Got RMSE {RMSE}')

    if verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device)
          y = y.to(device=device)
          scores = model(x)
          #preds = (torch.round(scores)).reshape(-1)
          preds = torch.argmax(scores,dim=1)
          num_correct += (preds == y).sum()
          num_samples += preds.size(0)
          num_c0 += ((preds ==y) * (preds == torch.zeros_like(y))).sum() 
          num_c1 += ((preds ==y) * (preds == 2*torch.ones_like(y))).sum() 
          num_0 += ((preds !=y) * (preds == torch.zeros_like(y))).sum() 
          num_1 += ((preds !=y) * (preds == torch.ones_like(y))).sum() 
          num_2 += ((preds !=y) * (preds == 2*torch.ones_like(y))).sum() 
          num_3 += ((preds !=y) * (preds == 3*torch.ones_like(y))).sum() 
          num_4 += ((preds !=y) * (preds == 4*torch.ones_like(y))).sum() 
          num_5 += ((preds !=y) * (preds == 5*torch.ones_like(y))).sum() 
          num_6 += ((preds !=y) * (preds == 6*torch.ones_like(y))).sum() 
          num_7 += ((preds !=y) * (preds > 6*torch.ones_like(y))).sum() 
        acc = float(num_correct) / num_samples 
        acc_c0 = float(num_c0) / num_samples 
        acc_c1 = float(num_c1) / num_samples 
        acc_0 = float(num_0) / num_samples 
        acc_1 = float(num_1) / num_samples 
        acc_2 = float(num_2) / num_samples 
        acc_3 = float(num_3) / num_samples 
        acc_4 = float(num_4) / num_samples 
        acc_5 = float(num_5) / num_samples 
        acc_6 = float(num_6) / num_samples 
        acc_7 = float(num_7) / num_samples 
        print(f'Got {num_correct:d} / {num_samples:d} correct {acc:.2f}')
        print(f'Got {num_c0:d} / {num_samples:d} correct {acc_c0:.2f} preds as 0')
        print(f'Got {num_c1:d} / {num_samples:d} correct {acc_c1:.2f} preds as 2')
        print(f'Got {num_0:d} / {num_samples:d} wrong {acc_0:.2f} preds as 0')
        print(f'Got {num_1:d} / {num_samples:d} wrong {acc_1:.2f} preds as 1')
        print(f'Got {num_2:d} / {num_samples:d} wrong {acc_2:.2f} preds as 2')
        print(f'Got {num_3:d} / {num_samples:d} wrong {acc_3:.2f} preds as 3')
        print(f'Got {num_4:d} / {num_samples:d} wrong {acc_4:.2f} preds as 4')
        print(f'Got {num_5:d} / {num_samples:d} wrong {acc_5:.2f} preds as 5')
        print(f'Got {num_6:d} / {num_samples:d} wrong {acc_6:.2f} preds as 6')
        print(f'Got {num_7:d} / {num_samples:d} wrong {acc_7:.2f} preds as larger than 6')
           
    return RMSE , MSE/len(dataloader)


def get_mean_of_dataloader(dataloader,model,device):
    num_samples = 0
    b = torch.zeros(1,device=device)
    model.eval()
    for x,y in dataloader:
        y = y.to(device=device,dtype=torch.float)
        # use sum instead of mean, what do you think?
        y_sum = y.sum(dim=0,keepdim=True)
        num_samples += y.shape[0]
        print(y.shape[0])
        b =b+y_sum
    return b/num_samples


def check_RMSE_CNN(dataloader,model, grid_space, device, verbose=False):
    MSE = 0
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
          scores = model(x)
          # preds = torch.argmax(scores,dim=1)
          # num_correct += (preds == y).sum()
          MSE += F.mse_loss(scores, y, reduce='sum')
          R_temp += F.mse_loss(Bfield_mean.expand_as(y), y, reduce='sum')
        #   num_samples += preds.size(0)
        # acc = float(num_correct) / num_samples 
        RMSE = torch.sqrt(MSE/num_samples/grid_space)

        Rsquare=1-MSE/R_temp/num_samples
        print(f'Got RMSE {RMSE}')

        
    #####################################################
    if verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device=device)
          y = y.to(device=device)
          scores = model(x)
          #preds = (torch.round(scores)).reshape(-1)
          preds = torch.argmax(scores,dim=1)
           
    return RMSE, MSE/len(dataloader)/grid_space,Rsquare

def check_accuary_density(dataloader,model,bins,range):
  num_correct = 0
  num_samples = 0
  density = torch.zeros(bins)
  correct_density = torch.zeros(bins)
  with torch.no_grad():
    for x,y,z in dataloader:
      x = x.to(device)
      y = y.to(device)
      z = z.to(device)
      preds = torch.argmax(model(x),dim=1)
      num_correct += (preds == y).sum()
      num_samples += preds.size(0)
      density = density + torch.histogram(z.cpu().double(),bins=bins,range = range)[0]
      z[preds!=y] = -100
      correct_density = correct_density + torch.histogram(z.cpu().double(),bins=bins,range = range)[0]

    acc = float(num_correct) / num_samples  
    acc_density = correct_density/density
    print(f'Got {num_correct:d} / {num_samples:d} correct {acc:.2f}')
  return (acc,acc_density)

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