import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = './results/sdlva_tb_sweep_results_sorted.csv'
data = pd.read_csv(file_path, delimiter=';', header=0)

x = data.iloc[:, 0]
y = data.iloc[:, 1]

plt.figure(figsize=(8, 6))
plt.plot(x, y, label="Vout vs. Vin")

plt.xscale('log')

plt.title('Output Chararcteristic; Vin = 1u-2.5V, f = 1GHz, Ideal Half-Wave Rectifier used')
plt.xlabel('Vin in V')
plt.ylabel('Vout in V')

plt.grid(True, which="both", ls="--")
plt.legend()

plt.show()
