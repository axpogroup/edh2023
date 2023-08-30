import unittest

import numpy as np

from utils.eval import reward_function, reward_sum

class TestRewardFunction(unittest.TestCase):
    def test_dV_m2_shunt_reactor_state(self):
        dV = np.array([-3, -2, -1, 0])
        shunt_reactor_state = np.array([True, True, True, True])
        expected_reward = np.array([-24.4, 0, 3.0, 3.0])
        self.assertTrue(np.allclose(reward_function(dV, shunt_reactor_state), expected_reward))
    
    def test_dV_p1_not_shunt_reactor_state(self):
        dV = np.array([1, 2, 3, 4])
        shunt_reactor_state = np.array([False, False, False, False])
        expected_reward = np.array([3, 0, -24.4, -24.4])
        self.assertTrue(np.allclose(reward_function(dV, shunt_reactor_state), expected_reward))

class TestRewardSum(unittest.TestCase):
    def test_no_weighing_factors(self):
        dV = np.array([-3, -4, 0, 1])
        shunt_reactor_state = np.array([True, True, False, False])
        expected_reward_sum = -24.4 + -24.4*(5/6) + 3*(2/3) + 3*0.5
        self.assertAlmostEqual(reward_sum(dV, shunt_reactor_state), expected_reward_sum)
    
    def test_weighing_factors(self):
        dV = np.array([-3, -4, 0, 1])
        shunt_reactor_state = np.array([True, True, False, False])
        weighing_factors = np.array([1, 1, 0.5, 0.5])
        expected_reward_sum = -24.4 + -24.4 + 3*0.5 + 3*0.5
        self.assertAlmostEqual(reward_sum(dV, shunt_reactor_state, weighing_factors), expected_reward_sum)
        

if __name__ == '__main__':
    unittest.main()