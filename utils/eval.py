from typing import Optional, Tuple, Union

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
        dV: Union[np.array, float], 
        shunt_reactor_state: Union[np.array, bool],
        ) -> np.array:
    dV_m2 = dV < -2.
    dV_m1 = dV >= -1.
    dV_p2 = dV > 2. 
    dV_p1 = dV <= 1.
    reward = (-24.4*dV_m2 + 3*dV_m1) * shunt_reactor_state \
           + (-24.4*dV_p2 + 3*dV_p1) * (1 - shunt_reactor_state)
           
    return reward


def reward_sum(
        dV: np.array, 
        shunt_reactor_state: np.array,
        weighing_factors: Optional[np.array] = None,
        ) -> float:
    if weighing_factors is None:
        weighing_factors = np.linspace(1, 0.5, len(dV))
    
    return np.sum(reward_function(dV, shunt_reactor_state) * weighing_factors)


def alternative_strategy_reward(
    dV_real: float,
    dV_pred: float,
    WQ_realized: float,
    shunt_reactor_sensitivity: float,
    reactive_power_range: [float, float] = [35, 90],
) -> Tuple[float, float, float]:
    """Calculates an alternative strategy based on voltage deviations to calculate the reward
    for shunt reactor operation.

    Args:
        dV (float): _description_
        WQ_realized (float): _description_
        shunt_reactor_sensitivity (float): _description_
        reactive_power_range (float, float], optional): _description_. Defaults to [35, 90].

    Returns:
        np.array: _description_
    """
    # TODO: write tests for this function
    
    # we calculate the reward based on a strategy that would be optimal for our predicted voltage
    _, virtual_optimal_reward, _, virtual_optimal_WQ = maximize_virtual_points(
        dV_pred, WQ_realized, shunt_reactor_sensitivity, reactive_power_range
    )
    # and what it would have been with the real voltage (corrected by the shunt reactor impact)
    virtual_realized_reward = reward_function(dV_real, virtual_optimal_WQ > 1.0)
    
    return virtual_realized_reward, virtual_optimal_reward, virtual_optimal_WQ


def maximize_virtual_points(
    dV: float,
    WQ: float,
    shunt_reactor_sensitivity: float,
    reactive_power_range: [float, float] = [35, 90],
    ) -> Tuple[float, float, float, float]:
    """Calculates alternative voltage deltas based on a rule of thumb for the impact of
    shunt reactors on the voltage. The alternative voltage deltas are used to calculate
    an alternative reward. If the alternative reward is higher than the original reward,
    the alternative reward and voltage are returned. Otherwise, the original reward 
    and voltage are returned.
    Shunt reactor reactive power is chosen with a bang-bang control approach to calculate
    the rewards if the shunt reactor is switched on.

    Args:
        dV (float): _description_
        WQ (float): _description_
        shunt_reactor_sensitivity (float, optional): _description_. Defaults to 0.0454.
        reactive_power_range (float, float], optional): _description_. Defaults to [35, 90].

    Returns:
        Tuple[float, float, float]: realized points, virtual maximal points, 
            virtual voltage delta with optimal reward, virtual reactive power
    """
    # TODO: write tests for this function
    # TODO: formulate this as an optimization problem with number of switches as constraint
    if WQ <= 1.0:
        virtual_dV_shunt_min = dV - shunt_reactor_sensitivity*reactive_power_range[0]
        virtual_dV_shunt_max = dV - shunt_reactor_sensitivity*reactive_power_range[1]
        virtual_reward_shunt_min = reward_function(virtual_dV_shunt_min, True)
        virtual_reward_shunt_max = reward_function(virtual_dV_shunt_max, True)
        reward_shunt_off = reward_function(dV, False)
        if (virtual_reward_shunt_max > virtual_reward_shunt_min) and (virtual_reward_shunt_max > reward_shunt_off):
            return reward_shunt_off, virtual_reward_shunt_max, virtual_dV_shunt_max, 90
        elif (virtual_reward_shunt_min > virtual_reward_shunt_max) and (virtual_reward_shunt_min > reward_shunt_off):
            return reward_shunt_off, virtual_reward_shunt_min, virtual_dV_shunt_min, 35
        else:
            return reward_shunt_off, reward_shunt_off, dV, WQ
    else:
        virtual_dV_shunt_off = dV + shunt_reactor_sensitivity*WQ
        virtual_reward_shunt_off = reward_function(virtual_dV_shunt_off, False)
        reward_shunt_on = reward_function(dV, True)
        if virtual_reward_shunt_off > reward_shunt_on:
            return reward_shunt_on, virtual_reward_shunt_off, virtual_dV_shunt_off, 0
        else:
            return reward_shunt_on, reward_shunt_on, dV, WQ


def virtual_voltages(
        dV: np.array,
        WQ: np.array,
        shunt_reactor_sensitivity: float,
        reactive_power_range: [float, float] = [35, 90],
    ) -> Tuple[np.array, np.array, np.array]:
    virtual_dV_shunt_off = dV + shunt_reactor_sensitivity*WQ
    virtual_dV_shunt_min = virtual_dV_shunt_off - shunt_reactor_sensitivity*reactive_power_range[0]
    virtual_dV_shunt_max = virtual_dV_shunt_off - shunt_reactor_sensitivity*reactive_power_range[1]
        
    return virtual_dV_shunt_off, virtual_dV_shunt_min, virtual_dV_shunt_max