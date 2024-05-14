from os import path
import unittest
from SumoEnvironment import SumoEnv
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
np.set_printoptions(suppress=True, precision=3, floatmode="fixed")
from Model import run
from stable_baselines3 import A2C

class TestSumoEnv(unittest.TestCase):
    def setUp(self):  # setup the variables here before every test
        self.env = SumoEnv() # not intialized as a vector environment, as local env functions 
                             # cannot be used other than Gymnasium functions

    def tearDown(self):  # after each test
        self.env.close()

    @ classmethod
    def tearDownClass(cls):  # after all tests are done
        pass

    def test_initializations(self):
      action = [0]*self.env.bus_num # not required np.array, since we only have one environment and do not use vector environment
      obs, rewards, done, *_  = self.env.step(action)
      state_length = self.env.info_states + 2*self.env.bus_num
      self.assertEqual(len(obs), state_length)
      self.assertFalse((obs == np.array([0.0]*state_length, dtype=np.float32)).all()) # 200 initialization steps are taken beforehand, all fields should be not 0.0
      self.assertEqual(rewards, -1) # only one environment/no vector environment meaning no multiple rewards handling needed
      self.assertFalse(done) # only one environment/no vector environment meaning .all() not needed

    def test_find_nearest_function(self):
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 3800), 123) # goes into first if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 10000), 123) # goes into first if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 950), 827) # goes into second if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 1800), 1742) # goes into second if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 3592), 3592) # goes into else if statement
      self.assertEqual(self.env.find_nearest([123, 827, 1742, 2702, 3592], 123), 123) # goes into else if statement

    def test_done_after_100_steps(self):
      self.env.max_steps = 100
      for step in range(self.env.max_steps):
        action = [0]*self.env.bus_num
        _, _, done, *_  = self.env.step(action)
        if step == self.env.max_steps:
          self.assertTrue(done)
        else:
          self.assertFalse(done)

    def test_reset(self):
        action = [0]*self.env.bus_num
        self.env.step(action)
        self.env.reset()
        obs, rewards, done, *_  = self.env.step(action)
        state_length = self.env.info_states + 2*self.env.bus_num
        self.assertTrue((obs == np.array([0.0]*state_length, dtype=np.float32)).all())
        self.assertEqual(rewards, -1)
        self.assertFalse(done)    

    # change constants before run to lower step sizes
    def test_run_average_wait_time_increases_per_init_step(self):
        # data = run(A2C, "A2C", "MlpPolicy")
        # (avg wait time, avg people at bus stops)
        data = [(0.000, 0.000), (0.125, 1.000), (0.125, 0.667), (0.375, 1.000),
        (0.625, 2.000), (0.625, 1.875), (0.875, 2.556), (1.125, 3.100),
        (1.250, 3.727)]
        x_values, _ = zip(*data)
        self.assertTrue(all(x_values[i] >= x_values[i-1] for i in range(1, len(x_values))))

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)