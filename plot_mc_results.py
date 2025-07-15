import os
import sys
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

simulations_dir = "./simulations"
results_dir = os.path.join(simulations_dir, "results")

if len(sys.argv) < 3:
    print("Error: Incorrect number of arguments.")
    print("Usage: python3 " + sys.argv[0] + " <csv_file> [<results_plot_list>]")
    print("Example: python3 " + sys.argv[0] + " inv_mc_tb_mc_results.csv [gain_passband_dB,fc_l,fc_u,GBW]")
    sys.exit(1)

datafile_name = sys.argv[1]
data_file = os.path.join(results_dir, datafile_name)

results_plot_list = sys.argv[2].strip('[]').lower().split(',')

# plot results
if len(results_plot_list) > 0:
    # make dictionary with results
    results_dict = {}
    with open(data_file, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Initialize dictionary with keys from the header
        for header in reader.fieldnames:
            results_dict[header] = []

        # Fill the dictionary
        for row in reader:
            for header in reader.fieldnames:
                results_dict[header].append(float(row[header]))

    # Set the number of columns for subplot grid
    n_cols = 2  # Change this to 1, 2, 3, etc.
    n_plots = len(results_plot_list)
    n_rows = math.ceil(n_plots / n_cols)

    # Create subplots
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
    axs = axs.flatten()  # Flatten in case of multiple rows/columns
    i = 0
    for var in results_plot_list:
        data = np.array(results_dict[var.lower()])
        mean = data.mean()
        std = data.std()
        axs[i].hist(data, bins=50, color='skyblue', edgecolor='black')
        axs[i].set_title(f"Histogram of {var}")
        axs[i].set_xlabel(f"{var}")
        axs[i].set_ylabel("Count")
        ymax = axs[i].get_ylim()[1]

        # Plot mean line (solid green)
        axs[i].axvline(mean, color='green', linestyle='-', linewidth=2)
        axs[i].text(mean, ymax * 0.95, 'Mean', color='green', rotation=90, verticalalignment='top', horizontalalignment='center')

        # Plot sigma lines (dashed red)
        for sigma_mult in [1, 2, 3]:
            pos = mean + sigma_mult * std
            neg = mean - sigma_mult * std

            axs[i].axvline(pos, color='red', linestyle='--', linewidth=1)
            axs[i].axvline(neg, color='red', linestyle='--', linewidth=1)

            # Labels for sigma lines with a slight vertical offset to avoid overlap
            y_pos = ymax * (1 - 0.1 * sigma_mult)

            axs[i].text(pos, y_pos, f'+{sigma_mult}σ', color='red', rotation=90, verticalalignment='top', horizontalalignment='right')
            axs[i].text(neg, y_pos, f'-{sigma_mult}σ', color='red', rotation=90, verticalalignment='top', horizontalalignment='left')

        # Set more x-axis ticks for better readability
        x_min = mean - 4 * std
        x_max = mean + 4 * std
        ticks = np.arange(x_min, x_max + std/2, std/2)
        axs[i].set_xticks(ticks)
        i = i + 1

    # Hide unused subplots
    for j in range(i, len(axs)):
        axs[j].axis('off')
    plt.tight_layout()
    plt.show()
