import numpy as np


def reward_function(dV, W_Q):
    """
    Calculates the financial reward for a substation from voltage and reactive energy (=reactive power for one hour).
    
    Args:
        dV: V_ist - V_soll [kV] 
        W_Q: reactive energy [Mvarh]
        
    Returns:
        financial reward
    """
    c_mat = dV*np.sign(W_Q) > - 1
    nc_mat = dV*np.sign(W_Q) < -2
    reward = 3*np.abs(W_Q)*c_mat - 21.8*np.abs(W_Q)*nc_mat
    return reward

def reward_function_simplified(dV):
    pass