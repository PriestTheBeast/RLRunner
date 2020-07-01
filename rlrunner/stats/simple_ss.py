from rlrunner.stats.base_stat_saver import BaseStatSaver
import matplotlib.pyplot as plt


class SimpleSS(BaseStatSaver):
	"""
	This is a simple stat saver that saves the number of steps done in each episode
	and the cumulative rewards received in each episode

	It also shows this information in 2 graphs for each (env, agent) pair

	A better implementation would probably only save and show info about "exploit episodes"
	"""

	def __init__(self):
		super().__init__()
		self.stats = {}

	def step_update(self, is_exploit_episode, where, who, when, what):
		"""
		stats = {env: {agent: [ run0[ episode0[ cumulative_rewards, steps_done], ...], run1[], ...], ...}, ...}
		so this is a dictionary of environments which values are
		a dictionary of agents which values are
		a list of runs which values are
		a list of episodes which values are
		the number of steps done and the cumulative rewards
		"""

		run_number, episode_number, step_number = when
		obs, action, reward, new_obs, done = what

		# gets dict of agents in env
		agents_in_env = get_info_or_create(self.stats, where, {})

		# gets list of runs for agent
		runs_for_agent = get_info_or_create(agents_in_env, who, [])

		# gets list of episodes in run
		if len(runs_for_agent) == run_number:
			runs_for_agent.append([])
		episodes_in_run = runs_for_agent[run_number]

		# get the episode info in episodes
		if len(episodes_in_run) == episode_number:
			episodes_in_run.append([0, 0])
		episode_info = episodes_in_run[episode_number]

		episode_info[0] += reward
		if done:
			episode_info[1] = step_number

	def show_info(self):
		for env, agents_in_env in self.stats.items():
			plt.figure()
			for agent, runs_for_agent in agents_in_env.items():
				steps_per_eps = {}
				for run in runs_for_agent:
					for epi_n, epi_info in enumerate(run):
						if epi_n not in steps_per_eps:
							steps_per_eps[epi_n] = []
						steps_per_eps[epi_n].append(epi_info[1])
				avg_step_per_eps = {key: sum(value) / len(value) for key, value in steps_per_eps.items()}
				plt.plot(tuple(avg_step_per_eps.keys()), tuple(avg_step_per_eps.values()), label=agent.name)
			plt.xlabel('episode')
			plt.ylabel('total steps in epi')
			plt.title(env.name)
			plt.legend()

		for env, agents_in_env in self.stats.items():
			plt.figure()
			for agent, runs_for_agent in agents_in_env.items():
				crewards_per_eps = {}
				for run in runs_for_agent:
					for epi_n, epi_info in enumerate(run):
						if epi_n not in crewards_per_eps:
							crewards_per_eps[epi_n] = []
						crewards_per_eps[epi_n].append(epi_info[0])
				avg_crewards_per_eps = {key: sum(value) / len(value) for key, value in crewards_per_eps.items()}
				plt.plot(tuple(avg_crewards_per_eps.keys()), tuple(avg_crewards_per_eps.values()), label=agent.name)
			plt.xlabel('episode')
			plt.ylabel('cumulative rewards in epi')
			plt.title(env.name)
			plt.legend()

		plt.show()


def get_info_or_create(source_dict, key, default_value):
	"""
	This returns the value of the key if it exists
	else it creates the key with the default value and returns it
	"""
	try:
		info = source_dict[key]
		return info
	except KeyError:
		info = source_dict[key] = default_value
		return info
