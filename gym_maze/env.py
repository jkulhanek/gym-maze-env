import gym
from gym import error, spaces, utils
from gym.utils import seeding
import gym.spaces
import numpy as np
import random

def _get_maze(**kwargs):
    return (7, "--+---G" \
        "--+-+++" \
        "S-+---+" \
        "--+++--" \
        "--+-+--" \
        "--+----" \
        "-----++" )

class MazeEnv(gym.Env):
    metadata = {'render.modes': ['rgb_array']}

    def __init__(self, **kwargs):
        super(MazeEnv, self).__init__(**kwargs)

        (self._maze_size, self._map_data) = _get_maze(**kwargs)
        self._random = random.Random()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(0, 255, (84, 84, 3), dtype=np.int8)

        (self._pos, self._goal_pos) = self._get_positions()

    def _get_pixel(self, x, y):
        data_pos = y * self._maze_size + x
        return self._map_data[data_pos]

    def _get_positions(self):
        for y in range(self._maze_size):
            for x in range(self._maze_size):
                p = self._get_pixel(x,y)
                if p == 'S':
                    start_pos = (x, y)
                elif p == 'G':
                    goal_pos = (x, y)

        return (start_pos, goal_pos)

    def _clamp(self, n, minn, maxn):
        if n < minn:
            return minn, True
        elif n > maxn:
            return maxn, True
        return n, False

    def _move(self, change_vector):
        (x, y) = self._pos
        dx, dy = change_vector
        new_x = x + dx
        new_y = y + dy

        new_x, clamped_x = self._clamp(new_x, 0, self._maze_size - 1)
        new_y, clamped_y = self._clamp(new_y, 0, self._maze_size - 1)

        hit_wall = False

        if self._get_pixel(new_x, new_y) == '+':
            new_x = x
            new_y = x
            hit_wall = True

        hit = clamped_x or clamped_y or hit_wall
        return (new_x, new_y), hit

    def _get_current_state(self):
        image = np.zeros((84, 84, 3), dtype=np.int8)

        for y in range(self._maze_size):
            for x in range(self._maze_size):
                p = self._get_pixel(x,y)
                if p == '+':
                    self._put_pixel(image, x, y, 1)

        self._put_pixel(image, self._pos[0], self._pos[1], 2)
        self._put_pixel(image, self._goal_pos[0], self._goal_pos[1], 3)
        return image

    def _put_pixel(self, image, x, y, item):
        colormap = [
            np.array([0, 0, 0]),
            np.array([255, 0, 0]),
            np.array([0, 255, 0]),
            np.array([0, 0, 255])
        ]
        for i in range(12):
            for j in range(12):
                image[12*y + j, 12*x + i, :] = colormap[item]
    
    def step(self, action):
        dx = 0
        dy = 0
        if action == 0: # UP
            dy = -1
        if action == 1: # DOWN
            dy = 1
        if action == 2: # LEFT
            dx = -1
        if action == 3: # RIGHT
            dx = 1

        self._pos, hit = self._move((dx, dy,))
        state = self._get_current_state()
    
        terminal = (self._pos == self._goal_pos)

        if terminal:
            reward = 1
        elif hit:
            reward = -1
        else:
            reward = 0

        return state, reward, terminal, {}

    def reset(self):
        (self._pos, self._goal_pos) = self._get_positions()

        return self._get_current_state()

    def seed(self, seed = None):
        self._random.seed(seed)

    def render(self, mode='rgb_array', close=False):
        if mode == 'rgb_array':
            return self._get_current_state()
        #elif mode is 'human':
        #   pop up a window and render
        else:
            super(MazeEnv, self).render(mode=mode)


class GoalMazeEnv(gym.GoalEnv, MazeEnv):
    metadata = {'render.modes': ['rgb_array']}

    def __init__(self, **kwargs):
        super(GoalMazeEnv, self).__init__(**kwargs)

        image_space = self.observation_space
        self.observation_space = gym.spaces.Dict(dict(
            observation = image_space,
            achieved_goal = image_space,
            desired_goal = image_space
        ))            

    def _iter_pos(self):
        for y in range(self._maze_size):
            for x in range(self._maze_size):
                p = self._get_pixel(x,y)
                if p in ['S', 'G', '-']:
                    yield (x, y)
                else:
                    pass

    def _get_positions(self):
        potentials = list(self._iter_pos())
        return tuple(self._random.sample(potentials, 2))

    def _get_current_state(self):
        image = np.zeros((84, 84, 3), dtype=np.int8)
        goal = np.zeros((84, 84, 3), dtype=np.int8)

        for y in range(self._maze_size):
            for x in range(self._maze_size):
                p = self._get_pixel(x,y)
                if p == '+':
                    self._put_pixel(image, x, y, 1)
                    self._put_pixel(goal, x, y, 1)

        self._put_pixel(image, self._pos[0], self._pos[1], 2)
        self._put_pixel(goal, self._goal_pos[0], self._goal_pos[1], 2)
        
        return dict(
            observation = image,
            achieved_goal = image,
            desired_goal = goal
        )
