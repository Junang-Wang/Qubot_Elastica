from sklearn.metrics import mean_squared_error
import pysindy as ps
import matplotlib.pyplot as plt
import numpy as np
# Make coefficient plot for threshold scan
def plot_pareto(coefs, opt, model, threshold_scan, x_test, t_test, u =None):
    dt = t_test[1] - t_test[0]
    mse = np.zeros(len(threshold_scan))
    mse_sim = np.zeros(len(threshold_scan))
    for i in range(len(threshold_scan)):
        opt.coef_ = coefs[i]
        mse[i] = model.score(x_test, t=dt, u=u,metric=mean_squared_error)
    #     x_test_sim = model.simulate(x_test[0, :], t_test, integrator="odeint", u = u)
        # if np.any(x_test_sim > 1e4):
        #     x_test_sim = 1e4
        # mse_sim[i] = np.sum((x_test[1:] - x_test_sim) ** 2)
    plt.figure()
    plt.semilogy(threshold_scan, mse, "bo")
    plt.semilogy(threshold_scan, mse, "b")
    plt.ylabel(r"$\dot{X}$ RMSE", fontsize=20)
    plt.xlabel(r"$\lambda$", fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True)
    # plt.figure()
    # plt.semilogy(threshold_scan, mse_sim, "bo")
    # plt.semilogy(threshold_scan, mse_sim, "b")
    # plt.ylabel(r"$\dot{X}$ RMSE", fontsize=20)
    # plt.xlabel(r"$\lambda$", fontsize=20)
    # plt.xticks(fontsize=16)
    # plt.yticks(fontsize=16)
    # plt.grid(True)