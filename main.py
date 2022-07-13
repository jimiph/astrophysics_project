from asyncore import read
from hashlib import new
from pdb import line_prefix
import pandas as pd
import glob
import csv

path_for_reading_crude_data = r"D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/long_period_variable/"
all_files = glob.glob(path_for_reading_crude_data + "/*.csv")

li = []
for file_name in all_files:
    df = pd.read_csv(file_name, index_col=False, header=0)
    li.append(df)
path_for_saving_resulting_files = r"D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/"
frame = pd.concat(li, axis=0, ignore_index=True)
concat_file_name = "concat_dataset"
frame.to_csv(path_for_saving_resulting_files+f"{concat_file_name}"+'.csv', index=False)

final_dataset_name = "final_dataset"

with open(path_for_saving_resulting_files+f'{concat_file_name}'+'.csv', 'r') as f:
    new_csv = []
    reader = csv.reader(f)
    for row in reader:
        if all(row):
            new_csv.append(row)
f.close()
final_df = pd.DataFrame(new_csv)
final_df.to_csv(path_for_saving_resulting_files+f'{final_dataset_name}'+'.csv', header=0, index=False)
