from Stick_QUBO import StickMaxLength
from Functions_StickProblem import get_activated_sticks, get_cumulated_stick_length
import numpy as np 
import plotly.figure_factory as ff
import neal
import pandas as pd

#Creating Problem Instance
length = np.random.randint(1,10,10).tolist()
max_length = 19

stick_max_length = StickMaxLength()
stick_max_length.gen_problems(length, max_length)
Final_Q = stick_max_length.gen_qubo_matrix()

#Solve QUBO using Simulated Annealing from dwave
sampler = neal.SimulatedAnnealingSampler()
sampleset = sampler.sample_qubo(Final_Q, num_reads = 5000, num_sweeps = 1000)
best_sample = sampleset.first.sample

#Convert activated variables into Chosen Containers
chosen_sticks = get_activated_sticks(length, best_sample, max_length)
cumulated_stick_length = get_cumulated_stick_length(chosen_sticks)

#Create Dataframe
df = pd.DataFrame([
     dict(Task = 'Container', Start = s, Finish = f)for s,f in cumulated_stick_length
    ])

#Plot Solutions
fig = ff.create_gantt(df,  bar_width = 0.4, show_colorbar=True)
fig.update_layout(xaxis_type='linear', autosize=False, width=800, height=300)
fig.show()