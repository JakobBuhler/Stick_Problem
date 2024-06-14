def get_obj_func_value(lengths, best_sample,max_length):
    obj_value = 0
    for i in range(len(lengths)):
        if best_sample[i]==1:
            obj_value += lengths[i]
    if obj_value > max_length:
        obj_value = 0
    return obj_value

def get_activated_sticks(lengths,best_sample,max_lengt):#not sure about this one yet
    activated_solution_vars = []
    for i in best_sample:
        if best_sample[i]==1:
            activated_solution_vars.append(i)   
    activated_solution_lengths = [lengths[i] for i in activated_solution_vars if i < len(lengths)]
    return activated_solution_lengths



def get_cumulated_stick_length(activated_solution_lengths):#not sure about this one 
    cumulative_lengths = []
    start = 0
    for i in activated_solution_lengths:
        start_finish = [start, start + i]
        start = start_finish[1]
        cumulative_lengths.append(start_finish)
    return cumulative_lengths