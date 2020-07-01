from abc import ABC, abstractmethod


# A convenient class for storing stats about the runs

class BaseStatSaver(ABC):

	def __init__(self, name=None):
		if name is None:
			self.name = self.__class__.__name__
		else:
			self.name = name

	@abstractmethod
	def step_update(self, is_exploit_episode, where, who, when, what):
		"""
		Save information/stats here
		where -> is the env/environment
		who -> is the agent
		when -> is the current tuple (run_number, episode_number, step_number), all int
		what -> the transition or tuple (obs, action, reward, new_obs, done)

		is_exploit_episode -> if the current episode is an exploit episode,
		depending on the implementation of the agent this could mean:
		1. that the information is as close from the agent's max performance as possible or
		2. is with the lowest amount of randomness possible or
		3. it could mean nothing or
		4. it could mean something else
		5. it means what you make it mean in the agent's implementation

		This is probably where the information for graphs and etc should be saved and maybe used
		"""
		pass

	@abstractmethod
	def show_info(self):
		"""
		This one is not called automatically by the runner, you need to call it manually
		whenever you want it to do whatever you implemented

		It is also where you might want to do something with the information you have collected
		"""
		pass

	def should_i_run_agent(self, env, agent, runs):
		"""
		In this method you can return False and the runner will skip the agent
		The purpose of this method is for people to be able to implement persistence in the info saved
		and use it conveniently

		a Useful example: you create a folder called "saved_info" or something
		After an agent finishes its runs you create a string ID for identifying the
		env, agent, relevant parameters, etc about which the runs are about
		Then you check to see if a file with that name already exists in the folder you created
		If no file exists then you create a file where you store the info about the runs with that string ID as the name
		Now this method can be super useful, because you can check if you have already done
		the runs you are going to do from the string ID, and if you have then you can just get the run info you stored,
		store it here as if you did the run and then skip the actual agent simulation
		Basically you can get the info of a previous simulation you did and stop repeating simulations just because you
		want to add 1 agent to the comparison/runner
		Check the Pickle library for easy storage and retrieval of data structures to/from files

		With this you can easily skip an agent for wte reason you have
		(such has already having run the agent and having its run simulation info)
		"""
		return True
