import threading

from rlrunner.agents.base_agent import BaseAgent
from rlrunner.envs.base_env import BaseEnv
from rlrunner.stats.base_stat_saver import BaseStatSaver
from rlrunner.termination.base_termination_condition import BaseTerminationCondition


class Runner:
	"""
	# This is the main class and the class you should instantiate
	# you will call methods from here to change the runner and add agents, etc
	# and then call the do_it() method to start the run simulation

	# the loop hierarchy is (Env -> Agent ->) Run -> Episode -> Step

	# Note: prints for seeing the current progress should be implemented in TC (termination condition) or
	# SS (StatSaver) or even the render() in Env
	"""
	envs = []
	agents = []
	termination_cond = None
	stat_saver = None

	def __init__(self, number_of_runs=1, max_step_number=1000000):
		self.number_of_runs = number_of_runs
		self.max_step_number = max_step_number

	def set_termination_condition(self, termination_cond):
		if not isinstance(termination_cond, BaseTerminationCondition):
			print("Error: TerminationCondition doesn't come from BaseTerminationCondition")
			return
		self.termination_cond = termination_cond

	def set_stat_saver(self, stat_saver):
		if not isinstance(stat_saver, BaseStatSaver):
			print("Error: StatSaver doesn't come from BaseStatSaver")
			return
		self.stat_saver = stat_saver

	def add_agent(self, agent):
		if not isinstance(agent, BaseAgent):
			print("Error: Agent doesn't come from BaseAgent")
			return
		self.agents.append(agent)

	def remove_agent(self, agent):
		self.agents.remove(agent)

	def add_env(self, env):
		if not isinstance(env, BaseEnv):
			print("Error: Env doesn't come from BaseEnv")
			return
		self.envs.append(env)

	def remove_env(self, env):
		self.envs.remove(env)

	def do_it(self, verbose=True):
		x = threading.Thread(target=self.make_run, daemon=True, args=[verbose])
		x.start()
		return x

	def make_run(self, verbose=True):
		if self.termination_cond is None:
			print("Error: There is no TerminationCondition, you should set one")
			return

		for env in self.envs:
			for agent in self.agents:
				if self.stat_saver is not None and not self.stat_saver.should_i_run_agent(env, agent, self.number_of_runs):
					continue

				agent.setup(env.action_space, env.observation_space)

				if verbose:
					print("Starting Runs for agent %s in env %s" % (agent.name, env.name))

				# loop of runs
				for run_number in range(self.number_of_runs):

					if verbose:
						print("Doing Run nr", run_number)

					# loop of episodes
					episode_number = -1
					active_run = True
					while active_run:
						episode_number += 1

						is_exploit_episode = self.termination_cond.is_exploit_episode(episode_number)
						obs = env.reset()

						# loop of steps
						for step_nr in range(self.max_step_number):
							env.render()

							action = agent.get_action(obs, is_exploit_episode)

							result = env.step(action)
							if len(result) == 4:
								new_observation, reward, done, _ = result
							else:
								new_observation, reward, done = result

							transition = (obs, action, reward, new_observation, done)
							agent.learn(transition)

							obs = new_observation
							self.termination_cond.update_info(episode_number, transition)
							if self.stat_saver is not None:
								self.stat_saver.step_update(is_exploit_episode, env, agent,
															(run_number, episode_number, step_nr), transition)
							if done:
								break

						active_run = not self.termination_cond.check_termination(episode_number)

						# 1. episode ends
					# 2. run ends
					agent.reset()
				# 3. runs with agent end / time for new agent
			# 4. agents with env end / time for new env
			env.close()
		# 5. all ends
		print()
		print("All done.")
