import os
import sys
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

simulations_dir = "./simulations"
results_dir = os.path.join(simulations_dir, "results")

if len(sys.argv) < 7:
    print("Error: Incorrect number of arguments.")
    print("Usage: python3 " + sys.argv[0] + " <csv_file> [<param_name_list>] [<results_plot_list>] [results_plot_contour_index] [results_plot_logx_index] [results_plot_logy_index]")
    print("Example: python3 " + sys.argv[0] + " inv_sweep_tb_sweep_results.csv [m1_w_val,m2_w_val] [gain_passband_dB,fc_l,fc_u,GBW] [3] [1,2] [2]")
    sys.exit(1)

datafile_name = sys.argv[1]
data_file = os.path.join(results_dir, datafile_name)

param_name_list = sys.argv[2].strip('[]').lower().split(',')
results_plot_list = sys.argv[3].strip('[]').lower().split(',')
results_plot_contour_index  = [int(x) for x in sys.argv[4].strip('[]').split(',') if x.strip()]
results_plot_logx_index     = [int(x) for x in sys.argv[5].strip('[]').split(',') if x.strip()]
results_plot_logy_index     = [int(x) for x in sys.argv[6].strip('[]').split(',') if x.strip()]

# plot results
if len(results_plot_list) > 0:
    df = pd.read_csv(data_file, delimiter=';')
    df_sorted = df.sort_values(by=param_name_list)

    # Set the number of columns for subplot grid
    n_cols = 2  # Change this to 1, 2, 3, etc.
    n_plots = len(results_plot_list)
    n_rows = math.ceil(n_plots / n_cols)

    # Create subplots
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
    axs = axs.flatten()  # Flatten in case of multiple rows/columns
    i = 0
    if len(param_name_list) == 1:
        for var in results_plot_list:
            axs[i].set_title(var)
            axs[i].grid(True, which='both', linestyle='--', linewidth=0.5)
            axs[i].minorticks_on()
            axs[i].set_xlabel(f"{param_name_list[0]}")
            axs[i].set_ylabel(f"{var}")
            var = var.lower()
            if i in results_plot_logx_index and i in results_plot_logy_index:
                axs[i].loglog(df_sorted[param_name_list[0]], df_sorted[var])
            elif i in results_plot_logx_index:
                axs[i].semilogx(df_sorted[param_name_list[0]], df_sorted[var])
            elif i in results_plot_logy_index:
                axs[i].semilogy(df_sorted[param_name_list[0]], df_sorted[var])
            else:
                axs[i].plot(df_sorted[param_name_list[0]], df_sorted[var])
            i = i + 1
        # Hide unused subplots
        for j in range(i, len(axs)):
            axs[j].axis('off')
        plt.tight_layout()
        plt.show()
    elif len(param_name_list) == 2:
        for var in results_plot_list:
            axs[i].set_title(var)
            axs[i].set_xlabel(f"{param_name_list[0]}")              
            axs[i].grid(True, which='both', linestyle='--', alpha=0.5)
            axs[i].minorticks_on()
            x = np.unique(np.array(df_sorted[param_name_list[0]]))
            y = np.unique(np.array(df_sorted[param_name_list[1]]))
            Z = np.array(df_sorted[var.lower()]).reshape(len(x), len(y)).T # shape: (len(y), len(x))
            if i in results_plot_contour_index:
                axs[i].set_ylabel(f"{param_name_list[1]}")
                X, Y = np.meshgrid(x,y)
                contour = axs[i].contourf(X, Y, Z, levels=10, cmap='viridis')
                cbar = fig.colorbar(contour, ax=axs[i])
                cbar.set_label(var)
            else:
                axs[i].set_ylabel(var)
                Z = Z.T
                if i in results_plot_logx_index and i in results_plot_logy_index:
                    for l, yl in enumerate(y):
                        axs[i].loglog(x, Z[:, l], label=f"{yl:.2g}")
                elif i in results_plot_logx_index:
                    for l, yl in enumerate(y):
                        axs[i].semilogx(x, Z[:, l], label=f"{yl:.2g}")
                elif i in results_plot_logy_index:
                    for l, yl in enumerate(y):
                        axs[i].semilogy(x, Z[:, l], label=f"{yl:.2g}")
                else:
                    for l, yl in enumerate(y):
                        axs[i].plot(x, Z[:, l], label=f"{yl:.2g}")
                axs[i].legend(title=param_name_list[1], loc='upper right')
            i = i + 1
        # Hide unused subplots
        for j in range(i, len(axs)):
            axs[j].axis('off')
        plt.tight_layout()
        plt.show()
    else:
        print("Warning: Plot not possible due to more than 2 parameter sweeps.")
