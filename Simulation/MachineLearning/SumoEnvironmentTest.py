from os import path
import unittest
from SumoEnvironment import SumoEnv
import numpy as np

np.set_printoptions(suppress=True, precision=3, floatmode="fixed")

class TestSumoEnv(unittest.TestCase):
    def setUp(self):  # setup the variables here before every test
        self.env = SumoEnv()
        self.env.reset()

    def tearDown(self):  # after each test
        self.env.close()

    @ classmethod
    def tearDownClass(cls):  # after all tests are done
        pass

    def test_initializations(self):
      action = [0]*self.env.bus_num
      obs, rewards, done, *_  = self.env.step(action)
      state_length = self.env.info_states + 2*self.env.bus_num
      self.assertEqual(len(obs), state_length)
      self.assertEqual((obs == np.array([0.0]*state_length, dtype=np.float32)).all(), True)
      self.assertEqual(rewards, -1)
      self.assertFalse(done)

    def test_find_nearest_function(self):
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 3800), 123) # goes into first if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 10000), 123) # goes into first if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 950), 827) # goes into second if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 1800), 1742) # goes into second if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 3592), 3592) # goes into else if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 123), 123) # goes into else if statement

    def test_all_has_driven(self):
      prev_distances = [0]*(self.env.bus_num-2)
      for _ in range(10):
        obs, *_ = self.env.step([1]*self.env.bus_num)
        for i in range(2, len(obs), 2):
          pass

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)