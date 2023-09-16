import numpy as np
from utils import eval
import itertools

def num_flips(given):
    flips = 0
    for i in range(1, len(given)):
        flips += abs(given[i] - given[i-1])
    return flips

def best_permutation(dV, shunt_states, reward_sum, best_array):
    replacement_values = [0.35, 0.90]
    one_indices = [i for i, val in enumerate(row) if val == 1]
    replacement_combinations = list(itertools.product(replacement_values, repeat=len(one_indices)))

    for combo in replacement_combinations:
        modified_array = original_array[:]
        for i, val in zip(one_indices, combo):
            modified_array[i] = val

        score = eval.reward_sum(dV, shunt_states, modified_array)
        if(score > reward_sum):
            reward_sum = score
            best_array = modified_array
        elif(score == reward_sum and num_flips(best_array) > num_flips(modified_array)):
            reward_sum = score
            best_array = modified_array
        
    return reward_sum, best_array

# TODO: Change DVk
def simulate_switch(dV, WQ, sensitivity):
    best_array = np.ones(96)
    reward_sum = eval.virtual_voltages(dV, WQ, sensitivity)
    
    for k in range(1, 96):
        S_ktemp = np.fliplr(np.tril(np.ones((96-k, 96-k)), -1))
        S_k = np.hstack((np.ones([S_ktemp.shape[0], k], S_ktemp.dtype)))
        S_kinv = np.subtract(np.ones(S_k.shape), S_k)
    
        dV_off, dV_min, dV_max = eval.virtual_voltages(dV, WQ, sensitivity)
        DVk = np.add(np.multiply(S_k, dV_on), np.multiply(S_kinv, dV_off))
        
        for i in range(DVk.shape[0]):
            reward_sum_temp, best_array_temp = best_permutation(DVk[i], S_k[i], reward_sum, best_array)
            if reward_sum_temp > reward_sum:
                reward_sum = reward_sum_temp
                best_array = best_array_temp

    return reward_sum, best_array
