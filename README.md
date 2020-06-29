# RL Runner

> An easy to use and expand framework for RL experimentation and run simulation

## About

I had some difficulty naming this project and ended up choosing RL runner, but some other options would be RL Agent runner, Agent comparator, RL Running System, Agent Running system, etc...
In the past I've wanted, both academically and for fun experimentations, to compare different RL agents, with different parameters and different environments, but didn't find anything, except gym which help with environments. So I made my own system for performing runs with different agents and environments, adding other features along as I found necessary and useful. In the end it was a mess of code, but code I that could be useful for other people that need what I also needed. So I wrote this RL running framework from the ground up with this in mind: as much freedom as possible for experimenting and doing what people want while providing a good foundation for building upon it.

## How it works

You create a runner object. You add agents, environments (and other things you might need) to the runner. You run the runner.

```python
from rlrunner.agents.simple_agent import SimpleAgent
from rlrunner.envs.simple_env import SimpleEnv
from rlrunner.termination.simple_tc import SimpleTC
from rlrunner.runner import Runner

runner = Runner()

runner.add_env(SimpleEnv())
runner.add_agent(SimpleAgent())

runner.set_termination_condition(SimpleTC())

run_thread = runner.do_it()
run_thread.join()
```

This is a simple example which simulates a SimpleAgent run in a SimpleEnv.

Basically there are abstract classes (BaseAgent, BaseEnv, etc) for you to extend. 
For example, the SimpleAgent class is a simple Q-learning implementation that extends the BaseAgent class. 
BaseEnv also extends the gym.Env class, so any Env you make that extends the BaseEnv is also a gym env and any gym env should be compatible with the runner.
The Runner do_it() method also creates a new thread, which will simulate the run, and returns the thread. In case you want to have multiple runners doing simulations at the same time.

## More info

The runner will do a run simulation for each Agent/Env pair it has, e.g. above the only pair was SimpleAgent/SimpleEnv so only one run simulation, if another agent was added then 2 run simulations would be made, for SimpleAgent/SimpleEnv and TheOtherAgent/SimpleEnv.

A run simulation constitutes of 3 loops, the loop of runs which has the loop of episodes which then has the loop of steps.
A step is one cycle of the simple RL loop.
An episode is a loop of steps. Generally an episode ends when the agent reaches a goal or after X steps.
A run is a loop of episodes. Generally a run ends after the agent is done learning the task/how to reach the goal or after X episodes.
A run simulation is a loop of runs. A run simulation ends after X runs.

I only talked about 2 of the main 4 components (BaseAgent and BaseEnv) and will now discuss the other 2: the TerminationCondition and the StatSaver.
The TerminationCondition is necessary and it is the class that will decide when a run should end. This exists in order to allow for implementations that observe the agent's performance and dynamically decide when to end an episode (when has an agent finish learning). The provided SimpleTC is a simple implementation that ends an episode after a set X number of episodes has passed.
The StatSaver is optional but highly recommended. It's an utility class made for the purpose of gathering, storing and 

More info then the one provided here is probably better to read and learn from the documentation in the files.
