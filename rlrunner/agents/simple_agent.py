import numpy as np

from rlrunner.agents.base_agent import BaseAgent
from gym.spaces import Discrete


class SimpleAgent(BaseAgent):
	"""
	This is a simple Q-learning agent and an example of a possible extension to the BaseAgent class

	Q_table is a dict where the observations/states are keys
	and the values are a list of the action Q_values for that obs/state
	The Q_value of action X is at the X index of the list
	so the Q_value of action '3' for obs "something" is
	Q_value = q_table["something"][3]
	or q_values = q_table["something"] and then Q_value = q_values[3]

	"""

	discount_factor = 0.9
	learning_rate = 0.5
	epsilon = 0.1
	action_space = None
	observation_space = None

	def __init__(self):
		super().__init__()
		self.q_table = {}

	def setup(self, action_space, observation_space):
		if not isinstance(action_space, Discrete):
			print("Error: The action space is not discrete")
			return
		self.action_space = action_space
		self.observation_space = observation_space

	def get_action(self, observation, is_exploit_episode):
		if not is_exploit_episode and np.random.random() < self.epsilon:
			return self.action_space.sample()

		q_values = self.get_q_values(observation)

		return q_values.index(max(q_values))

	def learn(self, transition):
		observation, action, reward, next_observation, done = transition

		obs_q_values = self.get_q_values(observation)

		if done:
			obs_q_values[action] += self.learning_rate * (reward - obs_q_values[action])

		else:
			future = max(self.get_q_values(next_observation))
			obs_q_values[action] += self.learning_rate * (reward + self.discount_factor * future - obs_q_values[action])

	def get_q_values(self, observation):
		try:
			q_values = self.q_table[observation]
		except KeyError:
			q_values = self.q_table[observation] = list(np.random.random(self.action_space.n))
		return q_values

	def reset(self):
		self.q_table = {}
