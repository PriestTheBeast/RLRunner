from abc import ABC, abstractmethod


class BaseAgent(ABC):
	"""This class is the base agent that you should extend in order to create your own agents."""

	def __init__(self, name=None):
		if name is None:
			self.name = self.__class__.__name__
		else:
			self.name = name

		# add possible initial setup

	@abstractmethod
	def setup(self, action_space, observation_space):
		"""
		in here you will receive the action_space and observation space
		this objects will be extensions of the object Space from gym
		you should perform whatever setup you might need with the spaces given

		You don't need to implement for all possible Space cases right away
		Start with just implementing the ones necessary given the envs you want
		"""
		pass

	@abstractmethod
	def get_action(self, observation, is_exploit_episode):
		"""
		add action choosing mechanism

		returns: the action chosen
		"""
		pass

	@abstractmethod
	def learn(self, transition):
		"""
		observation, action, reward, next_observation, episode_ended/done = transition
		add learning mechanism
		"""
		pass

	@abstractmethod
	def reset(self):
		"""
		this method is called in between runs and it should be used to reset any learning experience, etc
		it's objective is to be a cheaper reset then creating a new Agent object
		(don't really know if it is worth it to exist instead of just creating a new object, but it does for now)
		"""
		pass
