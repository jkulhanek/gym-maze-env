import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class MazeEnv(gym.Env):
    metadata = {'render.modes': ['rgb_array']}

    def __init__(self, **kwargs):
        super(MazeEnv, self).__init__(**kwargs)

    def step(self, action):
        ...

    def reset(self):
        ...

    def render(self, mode='rgb_array', close=False):
        if mode == 'rgb_array':
            return np.array(...) # return RGB frame suitable for video
        #elif mode is 'human':
        #   pop up a window and render
        else:
            super(MazeEnv, self).render(mode=mode) # just raise an exception