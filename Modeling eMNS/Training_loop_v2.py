#########################################################################
# Training loop
#############################################################################
import torch
from torch.nn.parallel import DistributedDataParallel
import torch.nn.functional as F
from early_stopping import EarlyStopping, EarlyDecay
from utils import Jacobian3, grad_loss_Jacobain, check_rmse_CNN, compute_discrete_curl, compute_discrete_divergence, grad_loss, get_mean_of_dataloader, gridData_reshape
from Neural_network import ResidualEMNSBlock_3d, BigBlock, Generative_net
import numpy as np
import ray
from ray import train, tune
from ray.train import Checkpoint
import tempfile, os
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

def adjust_learning_rate_cosine_v2(optimizer, lr_max, lr_min,max_epoch,tt,len_dataloader):
    """
    Cosine decay to the learning rate every iternation

    Return: None, but learning rate (lr) might be updated
    """
    phi = (5*tt)/(max_epoch*len_dataloader)
    decay_lr_max = 0.5**int(phi)
    for param_group in optimizer.param_groups:
        new_lr = lr_min+0.5*(decay_lr_max*lr_max-lr_min)*(1+np.cos(phi*np.pi))
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

def train_GM(config):
    """
    Train a model using torch API

    Inputs: 
    - model: A Pytorch Module giving the model to train
    - optimizer: An optimizer object we will use to train the model
    - epochs: A Python integer giving the number of epochs to train for

    Returns: model accuracies, prints model loss during training
    """
    #---------------unpack config---------------------
    # print(config)
    epochs = config["epochs"]
    verbose = config['verbose']
    lr_max = config['lr_max']
    lr_min = config['lr_min']
    DF = config['DF'] # whether using divergence free model
    grid_space = config['grid_space']
    schedule = config['schedule']
    learning_rate_decay = config['learning_rate_decay']
    maxB = config['maxB']
    minB = config['minB']
    device = config['device']
    train_set = config['train_set']
    valid_set = config['valid_set']
    
    ####################################################
    #--------------model construction------------------
    ####################################################
    model = construct_model_GM(config)

    

    # ####################################################
    # #---------------GPU parallel-----------------------
    # ####################################################
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)
        print(f'we are using {torch.cuda.device_count()} GPU')
    # if device == 'cuda':
    #     # device = 'cuda:'+str(torch.cuda.current_device())
    #     device = ray.train.torch.get_device()
    model.to(device)
    # # prepare model for training
    # model = train.torch.prepare_model(model)
    #####################################################
    #-------------------data loader----------------------
    #####################################################

    train_loader = torch.utils.data.DataLoader(dataset=train_set,batch_size=config['batch_size'],shuffle=True)
    valid_loader = torch.utils.data.DataLoader(dataset=valid_set,batch_size=config['batch_size'],shuffle=True)

    #####################################################
    #-------------------optimizer--------------------------
    #####################################################
    
    optimizer = torch.optim.Adam(
        [{'params': model.parameters()}], 
        lr= config['lr_max'], 
        weight_decay= config['L2_norm'], 
        betas=(0.5,0.99))
    
    #------------------------------------------------------
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
            # print(f"Outside: input size {x.size()}")
            # x,_,_ = max_min_norm(x,device)
            # y,_,_ = max_min_norm(y,device)
            optimizer.zero_grad() #zero out all of gradient
            if DF: 
                _, preds = Jacobian3(model(x))
            else:
                preds = model(x)
            # loss function in the paper "Modeling Electromagnetic Navigation Systems" 
            # loss= lamda_b*|y-preds| + lamda_g*| nabla(y) - nabla(preds)|
            l1_loss = F.l1_loss(preds,y)
            Grad_loss = grad_loss_Jacobain(preds,y)
            loss = l1_loss + Grad_loss
            loss.backward() # compute gradient of loss
            optimizer.step() #update parameters
            
            tt = t + epoch*len(train_loader) +1
            adjust_learning_rate_cosine(optimizer, lr_max, lr_min, epochs, tt, len(train_loader))
            # early_decay(loss, optimizer, learning_rate_decay)
            ###########################################################
            # print loss during training 
            if verbose and (tt % print_every == 1 or (epoch == epochs -1 and t == len(train_loader) -1) ) :
                print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}, l1 loss={l1_loss.item():.4f}, grad loss={Grad_loss.item():.4f}')
                rmse_val,mse_val,Rsquare = check_rmse_CNN(valid_loader,model,grid_space, device, DF,maxB=maxB,minB=minB)
                rmse,mse_train,R_TEMP = check_rmse_CNN(train_loader,model, grid_space, device, DF,maxB=maxB,minB=minB)
                rmse_val_history[tt//print_every] = rmse_val
                rmse_history[tt // print_every] = rmse 
                iter_history[tt // print_every] = tt 
                loss_history[tt // print_every] = loss.item()
                print()
                
            elif not verbose and (t == len(train_loader)-1):
                print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}, l1 loss={l1_loss.item():.4f}, grad loss={Grad_loss.item():.4f}')
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

        if epoch % (epochs-1) == 0: 
        # create checkpoint only at the begin and the end of epochs
            base_model = (model.module
                if isinstance(model, DistributedDataParallel) else model)
            checkpoint_dir = tempfile.mkdtemp()
            # load back training state
            checkpoint_data = {
                "epoch": epoch,
                "net_state_dict": base_model.state_dict(),
                'model': base_model
                # "optimizer_state_dict": optimizer.state_dict(),
            }
            torch.save(checkpoint_data, os.path.join(checkpoint_dir, "model.pt"))
            checkpoint = Checkpoint.from_directory(checkpoint_dir)
            # Send the current training result back to Tune
            train.report({'rmse_val':rmse_val.item(), 'rmse_train': rmse.item(), 'loss':loss.item()},checkpoint=checkpoint)
        else:
            train.report({'rmse_val':rmse_val.item(), 'rmse_train': rmse.item(), 'loss':loss.item()})

        

        adjust_learning_rate_sch(optimizer, learning_rate_decay, epoch, schedule)
        epoch_stop = epoch

    

    return rmse_history, rmse_val_history,loss_history, iter_history,mse_history, mse_val_history,epoch_stop,Rsquare
#-------------------------------------------------------------------------------------------------------
def construct_model_GM(config):
    num_input = config['num_input']
    skip_spacing = config['skip_spacing']
    num_repeat = config['num_repeat']
    num_block = config['num_block']
    output_shape = (3,16,16,16)
    SB_args = (64,64,skip_spacing,num_repeat) # (Cin, Cout, skip_spacing, num_repeat)
    BB_args = (2,num_block) # (scale_factor, num_block)
    SB_block = ResidualEMNSBlock_3d 
    BB_block = BigBlock


    model = Generative_net(SB_args, BB_args, SB_block, BB_block, num_input=num_input, output_shape= output_shape)
    return model


#-----------------------------------------------------------------



