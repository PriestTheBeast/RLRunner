import numpy as np

from gym.spaces import Discrete, Box

from rlrunner.envs.base_env import BaseEnv

"""
Simple navigation problem environment where the agent starts at S/Source and needs to learn how to reach
G/Goal, where blank spaces are positions the agent can be at and X's are walls

This class can also be easily extended to read the map from a file and
format it into a structure like the one used here
Doing this will allow one to quickly load different maps with just a file path as a variable and
a single class
"""


class SimpleEnv(BaseEnv):
	map = ("XXXXXXXXXXXXXXXXXX",
		   "XS      X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X                X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X        X",
		   "X       X       GX",
		   "XXXXXXXXXXXXXXXXXX")

	# Observations are going to be the x,y coords and actions (up,right,down,left)
	def __init__(self):
		super().__init__(action_space=Discrete(4),
						 observation_space=Box(-np.inf, np.inf, shape=(2,)))

		self.agent_pos = {"x": 0, "y": 0}

	def reset(self):
		# Where the S is
		self.agent_pos = {"x": 1, "y": 1}
		return tuple(self.agent_pos.values())

	# (0-up,1-right,2-down,3-left) this data structure isn't changed
	movement = {0: [0, -1], 1: [1, 0], 2: [0, 1], 3: [-1, 0]}

	def step(self, action: int):
		reward = -1
		done = False

		new_pos = self.agent_pos.copy()
		action_movement = self.movement[action]
		new_pos["x"] += action_movement[0]
		new_pos["y"] += action_movement[1]
		try:
			map_pos = self.map[new_pos["y"]][new_pos["x"]]
		except IndexError:
			print(new_pos["x"], new_pos["y"])
			raise IndexError

		if map_pos == "G":
			self.agent_pos = new_pos.copy()
			return tuple(self.agent_pos.values()), 100, True
		elif map_pos == "X":
			return tuple(self.agent_pos.values()), reward, done
		else:
			self.agent_pos = new_pos.copy()
			return tuple(self.agent_pos.values()), reward, done

	def close(self):
		pass

	def render(self, mode='human'):
		pass
