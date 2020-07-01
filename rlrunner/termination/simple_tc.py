from rlrunner.termination.base_termination_condition import BaseTerminationCondition


class SimpleTC(BaseTerminationCondition):
	"""
	This is a simple termination condition
	By default, the run ends after 200 episodes
	"""

	# 199 because it starts at 0
	def __init__(self, number_of_episodes=199):
		super().__init__()
		self.number_of_episodes = number_of_episodes

	def is_exploit_episode(self, episode_number):
		# This is already the default of the base class
		# so this is just here for the example
		# it could be super().is_exploit_episode(episode_number)
		return False

	def update_info(self, episode_number, transition):
		pass

	def check_termination(self, episode_number):
		return episode_number >= self.number_of_episodes
