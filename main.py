from fileinput import filename
import fractions
import pandas as pd
import glob
import os

path = r"D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/long_period_variable"
all_files = glob.glob(path + "/*.csv")

li = []
for file_name in all_files:
    df = pd.read_csv(file_name, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv('D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/long_period_variable/final_dataset.csv')


# os.makedirs('folder/subfolder', exist_ok=True)  
# df.to_csv('folder/subfolder/out.csv')  