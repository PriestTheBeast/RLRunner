from abc import ABC, abstractmethod

"""
Rant time
Generally an episode ends when the environment dictates it or
when it hits a number of steps previously and manually established

The number of runs is also previously and manually established
because runs are independent from each other

The number of episodes could also be previously and manually established
however episodes are not independent from each other,
so more thought could and maybe should be given on when to stop,
on when has the number of episodes been enough

That's the objective of this class, it's here to decide when should a run end

The hope is that the agent is learning and improving, and that the more episodes it has the better it becomes
but agents have different performances and learning curves,
and in order to compare them you might want to stop the runs when they reach a certain skill level,
instead of having them end at a specific episode number but with different skill levels

at the end of the day it's your choice, and this class exists so that that choice exists
Rant over

There are other things to talk about, but I will explain in the methods
"""


class BaseTerminationCondition(ABC):
	"""This class decides when a run should end."""

	def __init__(self, name=None):
		if name is None:
			self.name = self.__class__.__name__
		else:
			self.name = name

		# add possible initial setup

	@abstractmethod
	def is_exploit_episode(self, episode_number):
		"""
		This method should return True or False on whether the episode is an exploit episode or not
		An exploit episode is an episode where the agent should perform no exploration/only exploitation
		or/and should use as little to no randomness/rng as possible

		This method can, of course, be called by other methods of this class, but
		it's return value is also given to the agent when an action is needed
		and when a step update is send to the StatSaver
		"""
		return False

	@abstractmethod
	def update_info(self, episode_number, transition):
		"""
		In this method you will receive step information updates (transition) and the episode number
		With it you should be able to store whatever information you find relevant for
		calculating if the agent has done enough episodes/has stopped learning
		"""
		pass

	@abstractmethod
	def check_termination(self, episode_number):
		"""
		# Here you analyse the information you stored and calculate if the agent has done enough episodes
		# it should return True if the run should terminate
		"""
		pass
