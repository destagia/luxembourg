from chainer import Chain
import chainer.functions as F
import chainer.links     as L
import numpy             as np

class ActionValue(Chain):
    """
    CNN for deciding next line
    """
    def __init__(self, n_act):
        """
        What the parameters mean is discribed in DQN.__init__

        Convolution3D's information
        http://docs.chainer.org/en/stable/reference/links.html#convolution2d
        """
        super(ActionValue, self).__init__(
            l1=F.Linear(15, 1000),
            l2=F.Linear(1000, 1000),
            l3=F.Linear(1000, 1000),
            l4=F.Linear(1000, 1000),
            q_value=F.Linear(1000, n_act))

    def q_function(self, state):
        """
        Q-function
        """
        h1 = F.relu(self.l1(state))
        h2 = F.relu(self.l2(h1))
        h3 = F.relu(self.l3(h2))
        h4 = F.relu(self.l4(h3))
        return self.q_value(h4)
