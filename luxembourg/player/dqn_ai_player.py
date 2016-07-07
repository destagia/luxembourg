from chainer import cuda, Function, Variable, optimizers, serializers
from chainer import Chain

import copy
import pickle
import numpy             as np
import chainer.functions as F
import chainer.links     as L

from luxembourg import Board, Line, Point

class ActionValue(Chain):
    """
    CNN for deciding next line
    """

    def __init__(self, n_act):
        """
        What the parameters mean is discribed in DQN.__init__
        """
        super(ActionValue, self).__init__(
            l1=F.Convolution2D(5, 32, ksize=1, stride=2, nobias=False),
            l4=F.Linear(32, 64),
            q_value=F.Linear(64, n_act,
                             initialW=0.0*np.random.randn(n_act, 64).astype(np.float32))
        )

    def q_function(self, state):
        """
        Q-function
        """
        h1 = F.relu(self.l1(state))
        h4 = F.relu(self.l4(h1))
        return self.q_value(h4)
