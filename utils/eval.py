from typing import Optional

import numpy as np


def reward_function_old(dV: np.array, W_Q: np.array) -> float:
    """
    Calculates the financial reward for a substation from voltage and reactive energy (=reactive power for one hour).
    
    Args:
        dV: V_ist - V_soll [kV] 
        W_Q: reactive energy [Mvarh]
        
    Returns:
        reward/penalty resulting from the given voltage deviations and reactive energy
    """
    c_mat = dV*np.sign(W_Q) > - 1
    nc_mat = dV*np.sign(W_Q) < -2
    reward = 3*np.abs(W_Q)*c_mat - 24.4*np.abs(W_Q)*nc_mat
    return reward

def reward_function(
        dV: np.array, 
        shunt_reactor_state: np.array,
        ) -> np.array:
    
    dV_m2 = dV < -2.
    dV_m1 = dV >= -1.
    dV_p2 = dV > 2. 
    dV_p1 = dV <= 1.
    reward = (-24.4*dV_m2 + 3*dV_m1) * shunt_reactor_state \
           + (-24.4*dV_p2 + 3*dV_p1) * ~shunt_reactor_state
           
    return reward

def reward_sum(
        dV: np.array, 
        shunt_reactor_state: np.array,
        weighing_factors: Optional[np.array] = None,
        ) -> float:
    if weighing_factors is None:
        weighing_factors = np.linspace(1, 0.5, len(dV))
    
    return np.sum(reward_function(dV, shunt_reactor_state) * weighing_factors)