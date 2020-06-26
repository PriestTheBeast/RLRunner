# RL Runner

> An easy to use and expand framework for RL experimentation and run simulation

## About

I had some difficulty naming this project and ended up choosing RL runner, but some other options would be RL Agent runner, Agent comparator, RL Running System, Agent Running system, etc...
In the past I've wanted, both academically and for fun experimentations, to compare different RL agents, with different parameters and different environments, but didn't find anything, except gym which help with environments. So I made my own system for performing runs with different agents and environments, adding other features along as I found necessary and useful. In the end it was a mess of code, but code I that could be useful for other people that need what I also needed. So I wrote this RL running framework from the ground up with this in mind: as much freedom as possible for experimenting and doing what people want while providing a good foundation for building upon it.

## How it works

You create a runner object. You add agent, environments and other things you might need to the runner. You run the runner.

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
