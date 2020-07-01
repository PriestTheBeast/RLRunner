import gym

from rlrunner.envs.base_env import BaseEnv


class GymWrapperEnv(BaseEnv):
	"""Gym wrapper to add gym envs to the runner"""

	def __init__(self, gym_env: gym.Env):
		super().__init__(action_space=gym_env.action_space,
						 observation_space=gym_env.observation_space)

		self.gym_env = gym_env

	def reset(self):
		return self.gym_env.reset()

	def step(self, action):
		return self.gym_env.step(action)

	def close(self):
		self.gym_env.close()

	def render(self, mode='human'):
		self.gym_env.render(mode=mode)
