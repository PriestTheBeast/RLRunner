from gym import Env


class BaseEnv(Env):
	"""
	This class is the base environment that you should extend in order to create your own environments/worlds
	This class also extends the Env class from gym, so any gym environment is already supported by the runner
	and all your own environments that extend this will also be gym environments
	"""

	def __init__(self, name=None, action_space=None, observation_space=None):
		if name is None:
			self.name = self.__class__.__name__
		else:
			self.name = name

		# you need to provide some gym's space objects for this
		# http://gym.openai.com/docs/#spaces
		# also check the different spaces that exist so you can choose
		self.action_space = action_space
		self.observation_space = observation_space

		# add initial environment setup

	def reset(self):
		"""
		Reset the environment

		should return initial_observation
		"""
		raise NotImplementedError

	def step(self, action):
		"""
		Make an action in the environment and return the result

		should return new_observation, reward, done
		"""
		raise NotImplementedError

	def close(self):
		""" Performs any environment closing behaviour if needed """
		raise NotImplementedError

	def render(self, mode='human'):
		"""
		Implement this if you want some sort of render
		this is called every step
		"""
		raise NotImplementedError
