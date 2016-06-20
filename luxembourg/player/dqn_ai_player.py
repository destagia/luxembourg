from chainer import cuda, Function, Variable, optimizers, serializers
from chainer import Chain

import copy
import pickle
import numpy             as np
import scipy.misc        as spm
import chainer.functions as F
import chainer.links     as L

from luxembourg.board import Board


class ActionValue(Chain):
    """
    CNN for deciding next line
    """

    BOARD_POINT_NUM  = 15   # Input is the current board status
    LINE_PATTERN_NUM = 225  # Output is the specific pattern representing a line

    def __init__(self, n_act):
        """
        What the parameters mean is discribed in DQN.__init__
        """
        super(ActionValue, self).__init__(
            l1=F.Convolution2D(1, 32, ksize=8, stride=4, nobias=False, wscale=np.sqrt(2)),
            l2=F.Convolution2D(32, 64, ksize=4, stride=2, nobias=False, wscale=np.sqrt(2)),
            l3=F.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, wscale=np.sqrt(2)),
            l4=F.Linear(3136, 512, wscale=np.sqrt(2)),
            q_value=F.Linear(512, n_act,
                             initialW=np.zeros((n_act, 512),
                             dtype=np.float32))
        )

    def q_function(self, state):
        """
        Q-function
        """
        h1 = F.relu(self.l1(state))
        h2 = F.relu(self.l2(h1))
        h3 = F.relu(self.l3(h2))
        h4 = F.relu(self.l4(h3))
        return self.q_value(h4)

class ReplayBuffer:
    def __init__(self, states, actions, rewards, state_primes, episode_end_flags):
        self.__states = states
        self.__actions = actions
        self.__rewards = rewards
        self.__state_primes = state_primes
        self.__episode_end_flags = episode_end_flags

    def get_states(self):
        """
        State (array replaseting Board)
        """
        return self.__states

    def get_actions(self):
        """
        Action AI execute
        """
        return self.__actions

    def get_rewards(self):
        return self.__rewards

    def get_state_primes(self):
        return self.__state_primes

    def get_episode_end_flags(self):
        return self.__episode_end_flags


class DQN:

    # Hyper-Parameters
    GAMMA                      = 0.99     # Discount factor
    INITIAL_EXPLORATION        = 10 ** 4  # Initial exploratoin. original: 5x10^4
    REPLAY_SIZE                = 32       # Replay (batch) size
    TARGET_MODEL_UPDATE_FREQ   = 10 ** 4  # Target update frequancy. original: 10^4
    DATA_SIZE                  = 10 ** 5  # Data size of history. original: 10^6
    INPUT_SIZE                 = 15

    def __init__(self, n_act):
        """
        :param n_act: the number of actions, depending on which AI decides what to do
        """
        self.__step = 0
        self.__n_act = n_act

        self.__model = ActionValue(n_act).to_gpu()
        self.__model_target = copy.deepcopy(self.__model)

        self.__optimizer = optimizers.RMSpropGraves(lr=0.00025, alpha=0.95, momentum=0.95, eps=0.01)
        self.__optimizer.setup(self.__model)

        self.__replay_buffer = ReplayBuffer(
            np.zeros((DQN.DATA_SIZE, DQN.INPUT_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE, 1), dtype=np.float32),
            np.zeros((DQN.DATA_SIZE, DQN.INPUT_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE, 1), dtype=np.bool))


    def get_loss(self, state, action, reward, state_prime, episode_end):
        s = Variable(cuda.to_gpu(state))
        s_dash = Variable(cuda.to_gpu(state_prime))

        # Get Q-value
        q = self.__model.q_function(s)

        # Generate Target Signals
        tmp = self.__model_target.q_function(s_dash)
        tmp = list(map(np.max, tmp.data))
        max_q_prime = np.asanyarray(tmp, dtype=np.float32)
        target = np.asanyarray(copy.deepcopy(q.data.get()), dtype=np.float32)

        for i in range(DQN.REPLAY_SIZE):
            if episode_end[i][0]:
                _tmp = np.sign(reward[i])
            else:
                _tmp = np.sign(reward[i]) + DQN.GAMMA * max_q_prime[i]

            target[i, action[i]] = _tmp

        td = Variable(cuda.to_gpu(target)) = q
        td_tmp = td.data + 1000.0 * (abs(td.data) <= 1)
        td_clip = td * (abs(td.data) <= 1) + td / abs(td_tmp) * (abs(td.data) > 1)

        zero_val = Variable(cuda.to_gpu(np.zeros((DQN.REPLAY_SIZE, self.n_act), dtype=np.float32)))
        loss = F.mean_squared_error(td_clip, zero_val)
        return loss, q

class DqnAiPlayer:
    """
    AI created with DQN (Deep Q-Network)
    In the context of DQN, this is what so called Agent
    """
    def __init__(self):

    def get_line(self):

    def get_symbol(self):



