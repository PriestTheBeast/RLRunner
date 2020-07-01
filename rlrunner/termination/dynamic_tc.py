from rlrunner.termination.base_termination_condition import BaseTerminationCondition
from collections import deque


class DynamicTC(BaseTerminationCondition):
	"""
	This is a more complex and dynamic termination condition
	It will see if there has been sufficient progress in the last X episodes
	and if not it will assume the agent has stopped learning and terminate the run
	"""

	def __init__(self, epi_interval_for_progress=50, nr_exploits_in_interval=10):
		super().__init__()
		self.epi_interval_for_progress = epi_interval_for_progress
		self.nr_exploits_in_interval = nr_exploits_in_interval

		# this will calculate how frequent the exploit episodes will be to match the requirements wanted
		# in the default case it will be 50//10 = 5, so in every 5 episodes one of them will be an exploit episode
		self.exploit_every_x_epi = self.epi_interval_for_progress // self.nr_exploits_in_interval

		# info about the progress in the last X episodes
		self.info = deque(maxlen=self.nr_exploits_in_interval)

		self.cumulative_rewards = 0

	def is_exploit_episode(self, episode_number):
		return episode_number % self.exploit_every_x_epi == 0

	def update_info(self, episode_number, transition):
		# It will be more precise to measure the progress only from exploit episodes
		if self.is_exploit_episode(episode_number):
			_, _, reward, _, done = transition
			self.cumulative_rewards += reward
			if done:
				self.info.append(self.cumulative_rewards)
				self.cumulative_rewards = 0

	def check_termination(self, episode_number):
		# that "3" reward difference is kinda hardcoded for the simple_env reward function
		# but you get the point
		if episode_number > self.epi_interval_for_progress:
			avg = sum(self.info) / len(self.info)
			best_value = max(self.info)
			if best_value - avg < 3:
				return True
		return False
