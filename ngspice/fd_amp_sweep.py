import os
import itertools
import subprocess
from multiprocessing import Pool
import re
import csv
import numpy as np
import time

#params for optimization
#TODO adjust params
var1_name = "R1_val"
var1_val = np.arange(50, 1000, 100)
var1_val = var1_val.astype(str)
var2_name = "R2_val"
var2_val = np.arange(10, 200, 25)
var2_val = var2_val.astype(str)
var3_name = "R3_val"
var3_val = np.arange(50, 1000, 100)
var3_val = var3_val.astype(str)

#conditions
#TODO adjust conditions
cond1_name = "gain_1ghz_db"
cond1_min = 10
cond1_max = 15
cond2_name = "fc"
cond2_min = 1e9
cond2_max = 1e15
cond3_name = "gbw"
cond3_min = 1e9
cond3_max = 1e15
cond4_name = "gain_dc_db"
cond4_min = 10
cond4_max = 15

#TODO index sort results csv file descending
index_sort = 5

#start and end tag
results_start_tag = "results_opt_start"  
results_end_tag = "results_opt_end"    

netlist_name = "fd_amp"
simulations_dir = "./simulations"
results_dir = "./results"
final_result_file = os.path.join(results_dir, netlist_name + "_results.csv")
final_result_file_sorted = os.path.join(results_dir, netlist_name + "_results_sorted.csv")
netlist_path = os.path.join(simulations_dir, netlist_name + ".spice")

os.makedirs(simulations_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

if os.path.exists(final_result_file):
    os.remove(final_result_file)

with open(netlist_path, "r") as f:
    netlist = f.read()

#generate all combinations of params
all_combinations = list(itertools.product(var1_val, var2_val, var3_val)) #TODO adjust params

#split lst in n parts
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

#workers
def run_worker(args):
    param_list, worker_id = args
    cir_file = os.path.join(simulations_dir, f"{netlist_name}_worker_{worker_id}.cir")
    result_file = os.path.join(results_dir, f"{netlist_name}_worker_{worker_id}_results.txt")
    writeHeadings = True
    
    with open(result_file, "w") as results:
        writer = csv.writer(results, delimiter=";")
        for var1, var2, var3 in param_list: #TODO adjust params
            content = netlist.replace("{" + var1_name + "}", var1)\
                             .replace("{" + var2_name + "}", var2)\
                             .replace("{" + var3_name + "}", var3)

            with open(cir_file, "w") as f:
                f.write(content)

            try:
                output = subprocess.check_output(["ngspice", "-b", cir_file],
                                                 stderr=subprocess.STDOUT, text=True)

                #extract variables between results_start_tag and results_end_tag
                pattern = re.compile(
                    rf"{re.escape(results_start_tag)}(.*?){re.escape(results_end_tag)}",
                    re.DOTALL
                )
                match = pattern.search(output)
                if match:
                    block = match.group(1)
                    # extract variable name and value
                    data = {}
                    for line in block.strip().splitlines():
                        if '=' in line:
                            var, val = line.split('=')
                            data[var.strip()] = float(val.strip())
                    # write in csv file
                    if writeHeadings:
                        writer.writerow([var1_name, var2_name, var3_name] + list(data.keys())) #TODO adjust params
                        writeHeadings = False
                    if data[cond1_name] > cond1_min and data[cond1_name] < cond1_max and \
                       data[cond2_name] > cond2_min and data[cond2_name] < cond2_max and \
                       data[cond3_name] > cond3_min and data[cond3_name] < cond3_max and \
                       data[cond4_name] > cond4_min and data[cond4_name] < cond4_max:
                        writer.writerow([var1, var2, var3] + list(data.values())) #TODO adjust params
                else:
                    writer.writerow([var1, var2, var3, 'N/A', 'ERROR in receiving results']) #TODO adjust params

            except subprocess.CalledProcessError:
                writer.writerow([var1, var2, var3, 'N/A', 'ERROR in process handling']) #TODO adjust params
            os.remove(cir_file)

if __name__ == "__main__":
    start_time = time.time()
    
    num_workers = 16 #TODO adjust nr of workers 
    chunks = chunkify(all_combinations, num_workers)
    worker_inputs = [(chunk, i) for i, chunk in enumerate(chunks)]

    with Pool(num_workers) as pool:
        pool.map(run_worker, worker_inputs)

    # merge results of workers into a single file
    with open(final_result_file, "w") as out:
        for i in range(num_workers):
            part_file = os.path.join(results_dir, f"{netlist_name}_worker_{i}_results.txt")
            with open(part_file, "r") as part:
                lines = part.readlines()
                if i == 0:
                    out.writelines(lines)  # append first file incl. header
                else:
                    out.writelines(lines[1:]) # skip header
            os.remove(part_file)
            
    with open(final_result_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)
        data = list(reader)
        
    data.sort(key=lambda x: float(x[index_sort]), reverse=True)

    # create new file with sorted data
    with open(final_result_file_sorted, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(header)
        writer.writerows(data)
            
    end_time = time.time()
    runtime = end_time - start_time
    hours = int(runtime // 3600)
    minutes = int((runtime % 3600) // 60)
    seconds = int(runtime % 60)
    print(f"Runtime: {hours:02}:{minutes:02}:{seconds:02}")
