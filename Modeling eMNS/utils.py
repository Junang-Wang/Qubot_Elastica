import torch,ray,os
import matplotlib.pyplot as plt
import torch.nn.functional as F 
import numpy as np

def compute_discrete_curl(A_field, device):
    '''
    A_field: (batch, Dimensions, grid_x, grid_y, grid_z)
    '''
    batch, dimensions, grid_x, grid_y, grid_z = A_field.shape
    discrete_curl = torch.zeros(batch, dimensions, grid_x, grid_y, grid_z, device=device)

    # grad_x_A: dA/dx, grad_y_A: dA/dy, grad_z_A: dA/dz
    _,_, grad_x_A, grad_y_A, grad_z_A = torch.gradient(A_field,spacing=1.0)

    # curl A = (dA_z/dy - dA_y/dz) i + (dA_x/dz - dA_z/dx) j + (dA_y/dx - dA_x/dy) z
    discrete_curl[:,0] = grad_y_A[:,2] - grad_z_A[:,1]
    discrete_curl[:,1] = grad_z_A[:,0] - grad_x_A[:,2]
    discrete_curl[:,2] = grad_x_A[:,1] - grad_y_A[:,0]

    return discrete_curl

def compute_discrete_divergence(A_field):
    '''
    A_field: (batch, dimensions, grid_x, grid_y, grid_z)
    '''
    batch, dimensions, grid_x, grid_y, grid_z = A_field.shape
    discrete_div = torch.zeros(batch, 1, grid_x, grid_y, grid_z)
    
    # grad_x_A: dA/dx, grad_y_A: dA/dy, grad_z_A: dA/dz
    _,_, grad_x_A, grad_y_A, grad_z_A = torch.gradient(A_field,spacing=1.0)
    
    # div A = dA_x/dx  + dA_y/dy  + dA_z/dz 
    discrete_div[:,0] = grad_x_A[:,0] + grad_y_A[:,1] + grad_z_A[:,2]
    return discrete_div

def gridData_reshape(data):
    '''
    reshape data shape from ( dimension, grid_x, grid_y, grid_z) to (-1,dimension)
    '''
    return torch.flatten(data.permute(1,2,3,0), start_dim=0, end_dim=-2) #(-1, dimension)


def plot_3D_vector_field(position, vectorField, figsize=(5,5), length=1):
    '''
    Plot 3D vector field
    -----------input----------
    position: position of grids shape: (dimensions,grid_x,grid_y,grid_z)
    vectorField: shape (dimensions,grid_x,grid_y,grid_z)
    '''
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111,projection='3d') 
    p = gridData_reshape(position) #(-1, dimension)
    vector = gridData_reshape(vectorField) #(-1, dimension)

    ax.quiver(p[:,0], p[:,1], p[:,2], vector[:,0], vector[:,1], vector[:,2], length=length)
    plt.show()

def denorm(x_norm, Bmax, Bmin, device):
    '''
    This function de-normalize the max-min normalization
    x = 0.5*(x_norm+1)*(Bmax-Bmin) - Bmin
    '''
    x = 0.5*(x_norm+1)*(Bmax.expand_as(x_norm).to(device)-Bmin.expand_as(x_norm).to(device)) + Bmin.expand_as(x_norm).to(device)
    return x

def denorm_ray(x_norm, Bmax, Bmin):
    '''
    This function de-normalize the max-min normalization
    x = 0.5*(x_norm+1)*(Bmax-Bmin) - Bmin
    '''
    x = 0.5*(x_norm+1)*(Bmax.expand_as(x_norm)-Bmin.expand_as(x_norm)) + Bmin.expand_as(x_norm)
    return x


def max_min_norm(x,device):
    """
    Apply min-max normalization to the given tensor.
    
    :param tensor: A PyTorch tensor to be normalized.
    :return: A tensor with values scaled to the range [-1, 1], the max value and the min value.
    """
    min_val,_ = torch.min(x, dim=1, keepdim=True)
    max_val,_ = torch.max(x, dim=1 ,keepdim=True)
    normalized_x = 2*(x - min_val) / (max_val - min_val) - 1
    return normalized_x, max_val, min_val

def plot_ray_results(results, metrics_names,legend=False, ylim=None, xlim=None):

    # result_metrics = results.metrics
    # num_plot = 0
    # check if multi-result or a single result
    if type(results)==ray.tune.result_grid.ResultGrid:
        dfs = {result.path: result.metrics_dataframe for result in results}
    else:
        dfs = {results.path: results.metrics_dataframe}

    for metrics_name in metrics_names:

        ax = None 
        for data in dfs.values():
            ax = data[metrics_name].plot(ax=ax, legend=legend, ylim=ylim, xlim=xlim)

#-------------------------------------------------------------------------------------------------------

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



def check_rmse_CNN(dataloader,model, grid_space, device, DF, maxB=[],minB=[]):
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

    with torch.no_grad():
        for x,y in dataloader:
            x = x.to(device=device,dtype=torch.float)
            y = y.to(device=device,dtype=torch.float)
            num_samples += x.shape[0]
            if DF:
                _, scores = Jacobian3(model(x))
            else:
                scores = model(x)
            
            # compute mse and R2 by de-normalize data
            mse_temp += F.mse_loss(1e3*denorm(scores,maxB,minB,device), 1e3*denorm(y,maxB,minB, device) ,reduction='sum')
            R_temp += F.mse_loss(1e3*denorm(Bfield_mean.expand_as(y),maxB,minB,device), 1e3*denorm(y,maxB,minB,device), reduction='sum')


    rmse = torch.sqrt(mse_temp/num_samples/grid_space/3)

    Rsquare=1-mse_temp/R_temp/num_samples
    print(f'Got rmse {rmse}')

    return rmse, mse_temp/num_samples/grid_space/3, Rsquare

def check_rmse_ANN(dataloader, model, config):
    '''
    Check RMSE of ANN
    '''
    mse_temp = 0
    R_temp=0
    Rsquare=0
    num_samples = len(dataloader.dataset)
    device = config['device']
    maxB = config['maxB']
    minB = config['minB']
    backward = config['backward']
    

    # data = next(iter(dataloader))
    # no matter forward or backward_forward model, the output is 3D B field
    num_output = 3

    Bfield_mean=get_mean_of_dataloader(dataloader,model,device)

    model.eval() # set model to evaluation model 

    if backward:
        forward_model = config['forward_model']
        forward_model.eval()
        with torch.no_grad():
            for x,y in dataloader:
                x = x.to(device=device,dtype=torch.float)
                y = y.to(device=device,dtype=torch.float)

                Bfield = x[:, 3:]
                position = x[:, :3]
                current = model(x)
                
                # compute mse and R2 by de-normalize data
                mse_temp += F.mse_loss(denorm(Bfield,maxB, minB, device),  denorm(forward_model(torch.cat((current, position), axis =1)), maxB, minB, device) , reduction='sum')

                #TODO: fix R_temp
                R_temp += F.mse_loss(denorm(Bfield_mean.expand_as(y),maxB,minB,device), denorm(y,maxB,minB,device), reduction='sum')
    else:
        with torch.no_grad():
            for x,y in dataloader:
                x = x.to(device=device,dtype=torch.float)
                y = y.to(device=device,dtype=torch.float)

                scores = model(x)
                
                # compute mse and R2 by de-normalize data
                mse_temp += F.mse_loss(denorm(scores,maxB,minB,device), denorm(y,maxB,minB, device) ,reduction='sum')
                R_temp += F.mse_loss(denorm(Bfield_mean.expand_as(y),maxB,minB,device), denorm(y,maxB,minB,device), reduction='sum')

    mse = mse_temp/num_samples/num_output
    rmse = torch.sqrt(mse)

    Rsquare=1-mse_temp/R_temp/num_samples
    print(f'Got rmse {rmse}')

    return rmse, mse, Rsquare

def predict_check_rmse_ANN(dataloader, model, config):
    '''
    Check RMSE of ANN and return the prediction of the model
    '''
    mse_temp = 0
    R_temp=0
    Rsquare=0
    num_samples = len(dataloader.dataset)
    num_temp = 0
    current_mse_temp =0


    device = config['device']
    maxB = config['maxB']
    minB = config['minB']
    backward = config['backward']
    

    # data = next(iter(dataloader))

    # whether it's forward or backward_forward model, the output is 3D B field 
    num_output = 3
    prediction = torch.zeros(num_samples, num_output)
    

    Bfield_mean=get_mean_of_dataloader(dataloader,model,device)

    model.eval() # set model to evaluation model 

    if backward:
        forward_model = config['forward_model']
        forward_model.eval()

        current_L2 = 0
        current_backward_L2 = 0

        maxC = config['maxC']
        minC = config['minC']

        with torch.no_grad():
            for x,y in dataloader:
                x = x.to(device=device,dtype=torch.float)
                y = y.to(device=device,dtype=torch.float)

                Bfield = x[:, 3:]
                position = x[:, :3]
                current = model(x)

                B_est = forward_model(torch.cat((current, position), axis =1))
                
                # compute mse and R2 by de-normalize data
                mse_temp += F.mse_loss(denorm(Bfield,maxB, minB, device),  denorm(B_est, maxB, minB, device) , reduction='sum')

                current_mse_temp += F.mse_loss(denorm(current,maxC, minC, device),  denorm(y, maxC, minC, device) , reduction='sum')

                current_backward_L2 += F.mse_loss(denorm(current, maxC, minC, device), torch.zeros_like(current), reduction='sum') 

                current_L2 += F.mse_loss(denorm(y, maxC, minC, device), torch.zeros_like(current), reduction='sum') 

                #TODO: fix R_temp
                R_temp += F.mse_loss(denorm(Bfield_mean.expand_as(y),maxB,minB,device), denorm(y,maxB,minB,device), reduction='sum')

                prediction[num_temp:num_temp+x.shape[0]] = denorm(B_est, maxB, minB, device).to('cpu')
                num_temp += x.shape[0]
        
        C_mse = current_mse_temp/num_samples/12
        current_L2 = current_L2/num_samples
        current_backward_L2 = current_backward_L2/num_samples
        C_rmse = torch.sqrt(C_mse)
        print(f' current rmse: {C_rmse}, L2 before: {current_L2}, L2 after backward model: {current_backward_L2}')

    else:
        with torch.no_grad():
            for x,y in dataloader:
                x = x.to(device=device,dtype=torch.float)
                y = y.to(device=device,dtype=torch.float)

                B_est = model(x)
                
                # compute mse and R2 by de-normalize data
                mse_temp += F.mse_loss(denorm(B_est,maxB,minB,device), denorm(y,maxB,minB, device) ,reduction='sum')
                R_temp += F.mse_loss(denorm(Bfield_mean.expand_as(y),maxB,minB,device), denorm(y,maxB,minB,device), reduction='sum')

                prediction[num_temp:num_temp+x.shape[0]] = denorm(B_est, maxB, minB, device).to('cpu')
                num_temp += x.shape[0]

    mse = mse_temp/num_samples/num_output
    rmse = torch.sqrt(mse)

    Rsquare=1-mse_temp/R_temp/num_samples
    print(f'Got rmse {rmse}, num_samples {num_samples}')

    return prediction, rmse, mse, Rsquare
class estimate_test_set():
    '''
    This class estimate the error of the test set
    '''
    def __init__(self, checkpoint, test_set, train_loop_config) -> None:
        
        self.train_loop_config = train_loop_config
        #--------------------create test loader------------
        self.test_set = test_set
        self.test_loader = torch.utils.data.DataLoader(dataset=test_set,batch_size=train_loop_config['batch_size'],shuffle=True)

        # load checkpoint and model
        if checkpoint:
            with checkpoint.as_directory() as checkpoint_dir:
                self.model = torch.load(
                    os.path.join(checkpoint_dir, "model.pt"),map_location=train_loop_config['device'])['model']
        
    def fit(self):
        # estimate rmse for test set
        rmse_test, mse_test, R2_test = check_rmse_CNN(
            self.test_loader, self.model, self.train_loop_config['grid_space'], self.train_loop_config['device'], self.train_loop_config['DF'], self.train_loop_config['maxB'], self.train_loop_config['minB'])
        
        print(f'rmse for test set: {rmse_test:.4f}mT')
        print(f' mse for test set: {mse_test:.4f}mT')
        print(f'  R2 for test set: {R2_test:.4f}')
        return rmse_test, mse_test, R2_test
    
    def peek_z(self, z_plane_index):
        # for plotting a random choice sample in test set
        plot_index = np.random.choice(self.test_set.indices)
        plot_sample = self.test_set.dataset[plot_index]

        # prediction B field

        self.plot_B_pred = 1e3*denorm(self.model(torch.unsqueeze(plot_sample[0],0).to(device=self.train_loop_config['device'],dtype=torch.float)), self.train_loop_config['maxB'], self.train_loop_config['minB'], self.train_loop_config['device'])
        self.plot_B = 1e3*denorm(plot_sample[1].to(device=self.train_loop_config['device']), self.train_loop_config['maxB'], self.train_loop_config['minB'], self.train_loop_config['device'])

        ylables=['Bx(mT)','By(mT)','Bz(mT)']
        plot_rmse = torch.sqrt(F.mse_loss(self.plot_B, torch.squeeze(self.plot_B_pred,0), reduction='mean'))
        print(f'plot sample rmse: {plot_rmse:.4f}mT')

        f = plt.figure(figsize=(15,15))
        for i in range(1,4):

            B_est_temp =self.plot_B_pred[0,i-1,:,:,z_plane_index].detach()
            ax = f.add_subplot(3,2,2*i-1)
            img_plot = ax.imshow( B_est_temp.cpu() )    
            plt.ylabel(ylables[i-1])

            Bfield_temp = self.plot_B[i-1,:,:,z_plane_index]
            ax2 = f.add_subplot(3,2,2*i)
            img_plot=ax2.imshow(Bfield_temp.cpu())
            plt.colorbar(img_plot,ax=[ax,ax2])
            # plt.ylabel(ylables[i-1])
        plt.show()
    
    def peek_3D(self,length=0.1):
        from utils import plot_3D_vector_field
        x = torch.linspace(-10,10,16)
        y = torch.linspace(-10,10,16)
        z = torch.linspace(-10,10,16)
        print(x.shape)
        position = torch.cat(torch.meshgrid([x,y,z],indexing='ij')).reshape(3,16,16,16)
        print(position.shape)
        print(torch.squeeze(self.plot_B_pred,0).shape)
        plot_3D_vector_field(position[:,:,:,::15], torch.squeeze(self.plot_B_pred,0).detach()[:,:,:,::15].cpu(), length=length)

        plot_3D_vector_field(position[:,:,:,::15], self.plot_B[:,:,:,::15].cpu(), length=length)

#----------------------------------------------------------------
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

  j = torch.stack([dudx,dudy,dudz,dvdx,dvdy,dvdz,dwdx,dwdy,dwdz],axis=1)
  c = torch.stack([u,v,w],axis=1) #vorticity

  return j,c