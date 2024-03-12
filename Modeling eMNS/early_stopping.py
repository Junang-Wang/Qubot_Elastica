import numpy as np
import torch

class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0.0001):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), 'checkpoint.pt')	# 这里会存储迄今最优模型的参数
        self.val_loss_min = val_loss

class EarlyDecay:
    """Early decrease learning rate if loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0.02, lr_min = 1e-8):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            delta (float): Minimum percentage change in the monitored quantity to qualify as an improvement.
                            Default: 0.02
            lr_min (float): Minimum of lreaning rate
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_decay = False
        self.delta = delta
        self.lr_min = lr_min

    def __call__(self, loss, optimizer, lrd):

        score = -loss

        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score * (1-self.delta):

            self.counter += 1
            if self.verbose:
                print(f'EarlyDecay counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_decay = True
        else:
            self.best_score = score
            self.counter = 0
        
        if self.early_decay:
            print('-----------------------------------------------')
            self.adjust_learning_rate(optimizer, lrd, self.lr_min)
            self.early_decay = False

    def adjust_learning_rate(self, optimizer, lrd, lr_min):
        """
        Multiply lrd to the learning rate

        Return: None, but learning rate (lr) might be updated
        """
        for param_group in optimizer.param_groups:
            if param_group['lr'] > lr_min:
                print(f'lr decay from { param_group["lr"] } to {param_group["lr"]*lrd}')
                param_group['lr'] *= lrd
            else:
                print('lr reach to lr min, increase lr')
                param_group['lr'] *= 1.1