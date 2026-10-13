# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from SALib.analyze.sobol import analyze
from SALib.sample.sobol import sample
from SALib.test_functions import Ishigami
import numpy as np
import pandas as pd
#campionamento Saltelli
from SALib.sample import saltelli
from scipy.io import savemat
import subprocess


# Define the model inputs
problem = {
    'num_vars': 5,
    'names': ['Smax', 'alfa1', 'alfa2','d','dg'],
    'bounds': [[400, 1000],
               [0.3, 0.9],
               [0.3, 0.9],
               [0.3, 1],
               [0.3, 0.9]]

}

# #Generate samples
# param_values = sample(problem, 1024)
#
# Percorso del file - forse inutile
# file_path = r"D:\Project2026\Aleem_fromDelft\09022026_Sobol\simulation_results_1_Sobol_Saltelli.xlsx"
# # Leggi il primo foglio e solo le colonne di interesse
# df = pd.read_excel(
#     file_path,
#     sheet_name=0,
#     usecols=['Smax', 'alfa1', 'alfa2','d','dg']
# )
# # Controllo veloce
# print(df.head())
# param_values=df
#
param_values = saltelli.sample(problem, N=4096, calc_second_order=True)
# Salva in formato .mat
savemat('generations.mat',{'generations': param_values})
#run Budyko
matlab_exe = r"C:\Program Files\MATLAB\R2023a\bin\matlab.exe"
# 1 directory:
workdir = r"D:\Project2026\Aleem_fromDelft\Paper-2026\10072026_POST_GIORNATE\train_valid_Updated_13072026\16072026_AA_excel_optimazed_1-8__\SOBOL\C5_"
cmd = f"cd('{workdir.replace('\\','/')}'); code_5_pm_Sobol; exit"
subprocess.run([
    matlab_exe,
    "-batch",
    cmd
])

# #Run model (example)
# Y = Ishigami.evaluate(param_values)
#
#Run model (to obtain rmse or nnse)
# 2 directory:
file_path = r"D:\Project2026\Aleem_fromDelft\Paper-2026\10072026_POST_GIORNATE\train_valid_Updated_13072026\16072026_AA_excel_optimazed_1-8__\SOBOL\C5_\simulation_results_5_Sobol_Saltelli.xlsx"
# Leggi la colonna 'rmse' e sostituisci le celle vuote con NaN
df = pd.read_excel(
    file_path,
    sheet_name=0,
    header=None,         # trattiamo la riga 0 come dati
    na_values=['', ' '],  # considera vuote stringhe vuote o spazi
    keep_default_na=True  # mantiene anche i valori standard NaN di pandas
)

#prendi colonna (nnse)
Y = df.iloc[:, 6].to_numpy()  # array 1D
#

# Perform analysis
Si = analyze(problem, Y, print_to_console=True)

# # Print the first-order sensitivity indices
# print(Si['S1'])
#salva
# =========================
# EXPORT SOBOL RESULTS TO SINGLE EXCEL SHEET
# =========================
names = problem['names']

rows = []
# ---- S1 e ST (per parametro) ----
for i, name in enumerate(names):
    rows.append({
        'Type': 'Main',
        'Parameter_1': name,
        'Parameter_2': '',
        'S1': Si['S1'][i],
        'S1_conf': Si['S1_conf'][i],
        'ST': Si['ST'][i],
        'ST_conf': Si['ST_conf'][i],
        'S2': '',
        'S2_conf': ''
    })
# ---- S2 (interazioni) ----
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        rows.append({
            'Type': 'Interaction',
            'Parameter_1': names[i],
            'Parameter_2': names[j],
            'S1': '',
            'S1_conf': '',
            'ST': '',
            'ST_conf': '',
            'S2': Si['S2'][i, j],
            'S2_conf': Si['S2_conf'][i, j]
        })
df_out = pd.DataFrame(rows)
# Percorso output
# 3 directory:
output_file = r"D:\Project2026\Aleem_fromDelft\Paper-2026\10072026_POST_GIORNATE\train_valid_Updated_13072026\16072026_AA_excel_optimazed_1-8__\SOBOL\C5_\Sobol_results_single_sheet_5.xlsx"
# Scrittura Excel
df_out.to_excel(output_file, index=False)
print(f"Risultati Sobol salvati in un unico foglio:\n{output_file}")

