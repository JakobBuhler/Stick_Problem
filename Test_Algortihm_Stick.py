from Stick_QUBO import StickMaxLength
from Functions_StickProblem import get_activated_sticks,get_obj_func_value
import numpy as np
import neal
import pandas as pd
import matplotlib.pyplot as plt
import time

#set up DataFrame
df1 = pd.DataFrame(columns= ['Solver', 'Sample', 'ObjectiveValue', 'Index'])
df2 = pd.DataFrame(columns = ['Solver','Samper','Time','Index'])

for problem in range(5,14):
    #Create multiple Problem Instances
    length = np.random.randint(1,10,problem).tolist()
    max_length = 19 
    stick_max_length = StickMaxLength()
    stick_max_length.gen_problems(length, max_length)
    Final_Q = stick_max_length.gen_qubo_matrix()

    #Solve QUBO using Simulated Annealing from dwave:
    sampler = neal.SimulatedAnnealingSampler()
    start_time = time.time()
    sampleset = sampler.sample_qubo(Final_Q, num_reads = 5000, num_sweeps = 1000)
    end_time = time.time()
    best_sample = sampleset.first.sample

    #Clean Variables to set up Dataframe
    chosen_sticks = get_activated_sticks(length, best_sample, max_length)
    obj_func_value = get_obj_func_value(length, best_sample, max_length)
    total_time = end_time - start_time
    best_sample_str = str(best_sample)

    #dataframe for Objective Values
    df01 = pd.DataFrame({'Solver': 'SA', 'Sample': [best_sample_str], 'ObjectiveValue': [obj_func_value], 'Index' :[problem]})
    df1 = pd.concat([df1,df01],ignore_index= True)
    
    #dataframe for Time Values
    df02 = pd.DataFrame({'Solver': 'SA', 'Sample': [best_sample_str], 'Time': [total_time], 'Index' :[problem]})
    df2 = pd.concat([df2, df02])

#Rearranging DataFrame 
pivot_df1 = df1.pivot(index='Index', columns='Solver', values='ObjectiveValue')
pivot_df2 = df2.pivot(index='Index', columns = 'Solver', values = 'Time')

#Plotting Results
fig ,axs = plt.subplots(2, figsize = (10,8))
fig.suptitle('Luna Algortihm Tester Solver: TS')

for solver in pivot_df1.columns:
    axs[0].plot(pivot_df1.index, pivot_df1[solver], label=solver)
axs[0].set_title('Objective Value')
axs[0].axhline(y=max_length, color='r', linestyle='dashed', label=f'Target Value: {max_length}')  
axs[0].set_ylabel('Objective Value')
axs[0].legend(title='Solver')

for solver in pivot_df2.columns:
    axs[1].plot(pivot_df2.index, pivot_df2[solver], label=solver)
axs[1].set_title('Computing Time')
axs[1].set_ylabel('Time')
axs[1].set_xlabel('Index')
axs[1].legend(title='Solver')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
