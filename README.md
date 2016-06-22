# Many kinds of AI for Game of Last One

## Requirement

- Python 2.7.8+ (I use Python 2.7.10, but other minor version may cause no problem)

Less than 2.7.6 can not works at all!  
(Installing the dependencies will not be successful)

## Dependency

- bottle 0.12.9
- chainer 1.9.1
- filelock 2.0.6
- nose 1.3.7
- matplotlib 1.5.1
- numpy 1.11.0
- protobuf 2.6.1
- six 1.10.0

All dependencies will be installed with `requirements.txt`, executing the following command.

```shell
$ pip install -r requirements.txt
```

### Recommend

To avoid disrupting your environment, using **Virtualenv** is better.

```shell
$ pip install virtualenv
$ cd /path/to/luxembourg
$ virtualenv env # env is a conventional name. name whatever you want!
$ source ./env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ pip list -l # above-mentioned requirements will be displayed up!
```

## Monte Carlo AI

AI with Monte carlo approximation

## Deep Q-Network AI

I provide AI which use DQN, Deep Q-Network.

This AI (Agent in the DQN statement) works as follows.

    1. AI (Agent) get the current board (Observation) from Environment
    2. AI returns line to draw (Action) by considering with above board's state
    3. Environment get it, modify state with it, and return Reward to AI

# Reference

- [DQN-chainer](https://github.com/ugo-nama-kun/DQN-chainer)