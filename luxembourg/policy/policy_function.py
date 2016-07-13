from chainer import Chain
import chainer.functions as F
import chainer.links     as L
import numpy             as np

class PolicyFunction(Chain):

    def __init__(self, n_input, n_act):
        super(PolicyFunction, self).__init__(
            l1=F.Linear(n_input, 1000),
            # l2=F.Linear(1000, 1000),
            # l3=F.Linear(1000, 1000),
            # l4=F.Linear(1000, 1000),
            l5=F.Linear(1000, n_act))

    def __call__(self, state):
        """
        The param `state` is the collection.
        It has the value which indicate whether or not corresponding point is selected
        Indicator values:
            0 : the point is empty
            1 : the point has been already selected
        :state: 15-length array (In the case of 5-height game)
        """
        h1 = F.relu(self.l1(state))
        # h2 = F.relu(self.l2(h1))
        # h3 = F.relu(self.l3(h2))
        # h4 = F.relu(self.l4(h3))
        h5 = F.relu(self.l5(h1))
        return F.softmax(h5)
