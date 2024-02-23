#########################################################################
# Training loop
#############################################################################
import torch
import torch.nn.functional as F

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
def train_part(model,optimizer,train_loader,valid_loader, epochs = 1, learning_rate_decay =.1,weight_decay=1e-4, schedule=[], verbose=True):
    """
    Train a model using torch API

    Inputs: 
    - model: A Pytorch Module giving the model to train
    - optimizer: An optimizer object we will use to train the model
    - epochs: A Python integer giving the number of epochs to train for

    Returns: model accuracies, prints model loss during training
    """
    model = model.to(device='cuda')
    num_iters = epochs*len(train_loader)
    print_every = 100 
    adjust_epoch_count = 0
    if verbose:
        num_prints = num_iters // print_every + 1 
    else:
        num_prints = epochs 
    
    # initial accuracy history and iter history
    acc_history = torch.zeros(num_prints,dtype = torch.float)
    acc_val_history = torch.zeros(num_prints,dtype = torch.float)
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
        x = x.to(device='cuda',dtype=torch.float)
        y = y.to(device='cuda',dtype=torch.int64)
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
          acc_val = check_accuary(valid_loader,model)
          acc = check_accuary(train_loader,model)
          acc_val_history[tt//print_every] = acc_val
          acc_history[tt // print_every] = acc 
          iter_history[tt // print_every] = tt 
          loss_history[tt // print_every] = torch.round(loss,decimals=4).item()
          print()
          if (acc_val >= 0.995) and (epoch > 10):
            print('acc_val larger than 0.995, end the training loop')
            return acc_history, acc_val_history,loss_history, iter_history
            
        elif not verbose and (t == len(train_loader)-1):
          print(f'Epoch {epoch:d}, Iteration {tt:d}, loss = {loss.item():.4f}')
          acc_val = check_accuary(valid_loader,model)
          acc = check_accuary(train_loader,model)
          acc_val_history[epoch] = acc_val
          acc_history[epoch] = acc 
          iter_history[epoch] = tt 
          loss_history[epoch] = torch.round(loss,decimals=4).item()
          print()
          adjust_epoch_count += 1
          if epoch > 6 and adjust_epoch_count > 3:
            if loss_history[epoch-3:epoch+1].mean() >= 0.90*loss_history[epoch-7:epoch-3].mean():
              adjust_learning_rate(optimizer=optimizer,lrd= learning_rate_decay)
              print(f'{loss_history[epoch-3:epoch+1].mean():.2f} >= {0.95*loss_history[epoch-7:epoch-3].mean():.2f}')
              # adjust learning rate if loss has not decrease in 3 epochs
              adjust_epoch_count = 0
          if epoch > 10:    
            if (acc_val >= 0.995) and (loss_history[epoch-3:epoch+1].mean() >= 0.95*loss_history[epoch-10:epoch-3].mean()):
              print('acc_val reachs to 100%, end the training loop')
              return acc_history, acc_val_history,loss_history, iter_history
          
    return acc_history, acc_val_history,loss_history, iter_history

def check_accuary(dataloader,model,verbose=False):
    #if dataloader.dataset.train:
        #print("Checking accuracy on train or validation set")
    #else:
       # print('Checking accuracy on test set')
    
    num_correct = 0 
    num_samples = 0 
    num_c0 = 0 # the number of trivial cases (when the preds are correct)
    num_c1 = 0 # the number of trivial cases (when the preds are correct)
    num_0 = 0 # the number of trivial cases (when the preds are wrong)
    num_1 = 0 # the number of 1 cases (when the preds are wrong)
    num_2 = 0 # the number of 2 cases (when the preds are wrong)
    num_3 = 0 # the number of 3 cases (when the preds are wrong)
    num_4 = 0 # the number of 4 cases (when the preds are wrong)
    num_5 = 0 # the number of 5 cases (when the preds are wrong)
    num_6 = 0 # the number of 6 cases (when the preds are wrong)
    num_7 = 0 # the number of larger than 6 cases (when the preds are wrong)
    model.eval() # set model to evaluation model 
    if not verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device='cuda')
          y = y.to(device='cuda')
          scores = model(x)
          #preds = (torch.round(scores)).reshape(-1)
          preds = torch.argmax(scores,dim=1)
          num_correct += (preds == y).sum()
          num_samples += preds.size(0)
        acc = float(num_correct) / num_samples 
        print(f'Got {num_correct:d} / {num_samples:d} correct {acc:.2f}')

    if verbose:
      with torch.no_grad():
        for x,y in dataloader:
          x = x.to(device='cuda')
          y = y.to(device='cuda')
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
           
    return acc

def check_accuary_density(dataloader,model,bins,range):
  num_correct = 0
  num_samples = 0
  density = torch.zeros(bins)
  correct_density = torch.zeros(bins)
  with torch.no_grad():
    for x,y,z in dataloader:
      x = x.to('cuda')
      y = y.to('cuda')
      z = z.to('cuda')
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