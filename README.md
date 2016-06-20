# Many kinds of AI for Game of Last One

## Requirement

- Python 2.7.* (I use Python 2.7.6, but other minor version may cause no problem)

## Dependence

- Chainer 1.9.1
- Bottle 0.12.9

All dependency will be installed with `setup.py`, executing the following command.

```shell
$ pip install 
```

## Monte Carlo AI

AI with Monte carlo approximation


## Deep Q-Network AI

I provide AI which use DQN, Deep Q-Network.

This AI (Agent in the DQN statement) works as follows.

    1. AI (Agent) get the current board (Observation) from Environment
    2. AI returns line to draw (Action) by considering with above board's state
    3. Environment get it, modify state with it, and return Reward to AI