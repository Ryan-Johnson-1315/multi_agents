import gym
from gym import error, spaces, utils
from gym.utils import seeding

"""
    Environment where we will simulate a "Work Day". The work day
    involves tasks and workers. This will run the simulation
"""

class ProjEnv(gym.Env):
    def __init__(self):
        super().__init__()
    
    def step(self, action):
        pass

    def reset(self):
        pass
