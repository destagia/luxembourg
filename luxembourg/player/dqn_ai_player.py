from chainer         import cuda, Function, Variable, optimizers, serializers
from chainer         import Chain

import chainer.functions as F
import chainer.links as L

from luxembourg.board import Board


class ActionValue(Chain):
    """
    CNN for deciding next line
    """
    def __init__(self, n_history, n_act):
        super(ActionValue, self),__init__(
            l1=F.Convolution2D(15, 32, ksize=8, stride=4, nobias=False, wscale=np.sqrt(2)),
            l2=F.Convolution2D(32, 64, ksize=4, stride=2, nobias=False, wscale=np.sqrt(2)),
            l3=F.Convolution2D(64, 64, ksize=3, stride=1, nobias=False, wscale=np.sqrt(2)),
            l4=F.Linear(3136, 225, wscale=np.sqrt(2)),
            q_value=F.Linear(225, n_act,
                             initialW=np.zeros((n_act, 225),
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

class DQN:

    # Hyper-Parameters
    GAMMA                      = 0.99     # Discount factor
    INITIAL_EXPLORATION        = 10 ** 4  # Initial exploratoin. original: 5x10^4
    REPLAY_SIZE                = 32       # Replay (batch) size
    TARGET_MODEL_UPDATE_FREQ   = 10 ** 4  # Target update frequancy. original: 10^4
    DATA_SIZE                  = 10 ** 5  # Data size of history. original: 10^6
    IMG_SIZE                   = 84       # 84x84 image input (fixed)

    def __init__(self):
        self.__step  = 0
        self.__model = ActionValue(hoge, hoge)


class DqnAiPlayer:
    """
    AI created with DQN (Deep Q-Network)
    """
    def __init__(self):

    def get_line(self):

    def get_symbol(self):



