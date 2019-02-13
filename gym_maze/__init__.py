from gym.envs.registration import register
from env import MazeEnv

register(
    id='Maze-v0',
    entry_point='gym_maze:MazeEnv',
)