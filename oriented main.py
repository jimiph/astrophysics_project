import pandas as pd
import glob
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp

class varialble_star:

    def __init__(self, path_for_reading_crude_data = "D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/long_period_variable/",
     path_for_saving_resulting_files = "D:/University Cources/BS/6/astrophysics/astrophysics project/crude data/",
     path_for_saving_figs = "D:/University Cources/BS/6/astrophysics/astrophysics project/figures",
     concat_file_name = "concat_dataset", final_dataset_name = "final_dataset"):
        self.path_for_reading_crude_data = path_for_reading_crude_data
        self.path_for_saving_resulting_files = path_for_saving_resulting_files
        self.concat_file_name = concat_file_name
        self.final_dataset_name = final_dataset_name
        self.path_for_saving_figs = path_for_saving_figs
        self.cut_off = 8
        self.is_necessary_files_made = False
        self.make_final_dataset()
        
    def make_final_dataset(self):

        all_files = glob.glob(self.path_for_reading_crude_data + "/*.csv")
        li = []
        for file_name in all_files:
            df = pd.read_csv(file_name, index_col=False, header=0)
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.to_csv(self.path_for_saving_resulting_files+f"{self.concat_file_name}"+'.csv', index=False)
        
        with open(self.path_for_saving_resulting_files+f'{self.concat_file_name}'+'.csv', 'r') as f:
            new_csv = []
            reader = csv.reader(f)
            for row in reader:
                if all(row):
                    new_csv.append(row)
        f.close()
        final_df = pd.DataFrame(new_csv)
        final_df.to_csv(self.path_for_saving_resulting_files+f'{self.final_dataset_name}'+'.csv', header=0, index=False)
        self.is_necessary_files_made = True

    def make_diagram_Mv_per_logP(self):

        if self.is_necessary_files_made:

            full_path = self.path_for_saving_resulting_files + self.final_dataset_name + ".csv"
            data_frame = pd.read_csv(full_path)
            data_list = data_frame.T.values.tolist()    
            abs_mag_bol_good = []
            bolometric_corr_good = []
            P_s_good = []
            Mv_s = np.zeros(data_frame.shape[0]-1)
            for i in range(data_frame.shape[0]-1):
                cutt_off = self.cut_off

                if  np.abs(data_list[2][i])/np.abs(data_list[3][i])>cutt_off and np.abs(data_list[5][i])/np.abs(data_list[6][i])>cutt_off \
                    and np.abs(data_list[7][i])/np.abs(data_list[8][i])>cutt_off:
                    abs_mag_bol_good.append(data_list[2][i])
                    bolometric_corr_good.append(data_list[5][i])
                    P_s_good.append(1/data_list[7][i])
            Mv_s = np.array(abs_mag_bol_good) - np.array(bolometric_corr_good)
            slope, intercept, r, p, se = sp.linregress(np.log10(P_s_good), Mv_s)
            print('The function make_diagram_Mv_per_logP:', f'Slope of best fitted line is {slope}', f'Intercept of best fitted line is {intercept}')

            plt.scatter(np.log10(np.array(P_s_good)), Mv_s, s=1)
            plt.xlabel(r'$\log(P)$')
            plt.ylabel(r'$M_{v}$')
            plt.title(r'$M_{v}$'+ ' per' + 'Log of Period' + ' of' + ' The Star')
            plt.plot(np.log10(np.array(P_s_good)), slope*np.log10(np.array(P_s_good))+intercept, 
                    label='Fit with {:.4} '.format(slope)+r'$\log(P)$'+'+ {:.4}'.format(intercept), c='r')
            plt.legend()
            plt.savefig(self.path_for_saving_figs+'/Mv_s_per_log(P).png')
            plt.show()

    def make_diagram_period_disturb(self):

        if self.is_necessary_files_made:

            full_path = self.path_for_saving_resulting_files + self.final_dataset_name + ".csv"
            data_frame = pd.read_csv(full_path)
            data_list = data_frame.T.values.tolist()    
            P_s = []

            for i in range(data_frame.shape[0]-1):
                if np.abs(data_list[7][i])/np.abs(data_list[8][i])>self.cut_off:
                    P_s.append(1/data_list[7][i])

            plt.hist(P_s, 200)
            num_s, P_s, _ = plt.hist(P_s, 200)
            max_num = num_s.max()
            index = np.where(num_s==max_num)

            plt.xlabel('Period (days)')
            plt.ylabel('Number of Stars')
            plt.title(f'Most probable period is {P_s[index]}')
            plt.savefig(self.path_for_saving_figs+'/P_s_disturb.png')
            plt.show()



    def make_diagram_RSG_disturb(self):

        if self.is_necessary_files_made:

            full_path = self.path_for_saving_resulting_files + self.final_dataset_name + ".csv"
            data_frame = pd.read_csv(full_path)
            data_list = data_frame.T.values.tolist()    
            count_rsg = 0

            for i in range(data_frame.shape[0]-1):
                if data_list[4][i]:
                    count_rsg += 1

            count_non_rsg = data_frame.shape[0] - count_rsg - 1
            status = ['RSG', 'Not RSG']
            counts = [count_rsg, count_non_rsg]

            plt.bar(status, counts, color='green')
            plt.title("Distribution of Red Supergiants")
            plt.savefig(self.path_for_saving_figs+'/rsg_disturb.png')
            plt.show()


star = varialble_star()
star.make_diagram_Mv_per_logP()
# star.make_diagram_RSG_disturb()
# star.make_diagram_period_disturb()