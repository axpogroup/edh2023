import unittest

from utils.eval import reward_function

class TestRewardFunction(unittest.TestCase):
    def test_reward_function(self):
        dV = -1.5
        W_Q = 10
        expected_reward = dV*W_Q*21.8
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        
        dV = 0.5
        W_Q = 10
        expected_reward = dV*W_Q*3.0
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        
        dV = -0.5
        W_Q = 10
        expected_reward = 30
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        
        dV = -1.5
        W_Q = -10
        expected_reward = dV*W_Q*21.8
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        
        dV = -0.5
        W_Q = -10
        expected_reward = dV*W_Q*3.0
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        
        dV = 0.5
        W_Q = -10
        expected_reward = 30
        self.assertEqual(reward_function(dV, W_Q), expected_reward)
        

if __name__ == '__main__':
    unittest.main()