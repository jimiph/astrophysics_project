
from cProfile import label
import pandas as pd
import glob
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp

    
def make_final_dataset(path_for_reading_crude_data = "D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/long_period_variable/",
    path_for_saving_resulting_files = "D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/",
    concat_file_name = "concat_dataset", final_dataset_name = "final_dataset"):
    
    all_files = glob.glob(path_for_reading_crude_data + "/*.csv")
    li = []
    for file_name in all_files:
        df = pd.read_csv(file_name, index_col=False, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv(path_for_saving_resulting_files+f"{concat_file_name}"+'.csv', index=False)
    with open(path_for_saving_resulting_files+f'{concat_file_name}'+'.csv', 'r') as f:
        new_csv = []
        reader = csv.reader(f)
        for row in reader:
            if all(row):
                new_csv.append(row)
        # new_csv.pop(0)
    f.close()
    final_df = pd.DataFrame(new_csv)
    final_df.to_csv(path_for_saving_resulting_files+f'{final_dataset_name}'+'.csv', header=0, index=False)
    return path_for_saving_resulting_files, final_dataset_name


# print(make_final_dataset())
def make_diagram_Mv_per_logP():

    path_for_saving_resulting_files, final_dataset_name = make_final_dataset()
    full_path = path_for_saving_resulting_files + final_dataset_name + ".csv"
    data_frame = pd.read_csv(full_path)
    data_list = data_frame.T.values.tolist()    
    abs_mag_bol = np.zeros(data_frame.shape[0]-1)
    abs_mag_bol_good = []
    bolometric_corr = np.zeros(data_frame.shape[0]-1)
    bolometric_corr_good = []
    P_s = np.zeros(data_frame.shape[0]-1)
    P_s_good = []
    Mv_s = np.zeros(data_frame.shape[0]-1)
    for i in range(data_frame.shape[0]-1):
        abs_mag_bol[:][i] = data_list[2][i]
        bolometric_corr[:][i] = data_list[5][i]
        P_s[:][i] = data_list[7][i]
        cutt_off = 8
        if np.abs(data_list[2][i])/np.abs(data_list[3][i])>cutt_off and np.abs(data_list[5][i])/np.abs(data_list[6][i])>cutt_off \
            and np.abs(data_list[7][i])/np.abs(data_list[8][i])>cutt_off:
            abs_mag_bol_good.append(data_list[2][i])
            bolometric_corr_good.append(data_list[5][i])
            P_s_good.append(1/data_list[7][i])
    # print(abs_mag_bol[0:10])
    # print(P_s[0:10])
    # Mv_s = abs_mag_bol - bolometric_corr
    Mv_s = np.array(abs_mag_bol_good) - np.array(bolometric_corr_good)
    slope, intercept, r, p, se = sp.linregress(np.log10(P_s_good), Mv_s)
    
    print(slope, intercept)
    plt.scatter(np.log10(np.array(P_s_good)), Mv_s, s=1)
    plt.xlabel(r'$\log(P)$')
    plt.ylabel(r'$M_{v}$')
    plt.title(r'$M_{v}$'+ ' per' + ' Period' + ' of' + ' The Star')
    plt.plot(np.log10(np.array(P_s_good)), slope*np.log10(np.array(P_s_good))+intercept, 
             label='Fit with {:.4} '.format(slope)+r'$\log(P)$'+'+ {:.4}'.format(intercept), c='r')
    plt.legend()
    plt.show()
        

    # print(data_frame.shape[0])

# make_diagram_Mv_per_logP()

def make_diagram_log_L_per_P():

    pass

def make_diagram_period_disturb():

    pass

def make_diagram_RSG_disturb():

    pass


