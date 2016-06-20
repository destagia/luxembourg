# Many kinds of AI for Game of Last One

## Requirement

- Python 2.7.* (I use Python 2.7.11, other minor version may be no problem)

## Dependence

- Chainer

All dependency will be installed with `setup.py`, executing the following command.

```shell
$ python setup.py install
```

## DQN AI

I provide AI which use DQN, Deep Q-Network.

This AI (Agent in the DQN statement) works as follows.

    1. AI (Agent) get the current board (Observation) from Environment
    2. AI returns line to draw (Action) by considering with above board's state
    3. Environment get it, modify state with it, and return Reward to AI