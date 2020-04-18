import gym
from gym import error, spaces, utils
from gym.utils import seeding

# from rl_env.gym_work.envs.TypeDefs import *
from rl_env.gym_work.envs.types import *


"""
    This is the open gym environment
"""
class WorkEnv(gym.Env):
    def __init__(self, workers):
        self.state = []

        self.workers = workers # List of the worker Objects


    def step(self, action):
        pass
    
    def reset(self):
        print(f'RESET CALLED')
        pass

    def get_reward(self):
        pass

