from chainer import cuda, Function, Variable, optimizers, serializers
from chainer import Chain
import chainer.functions as F
import chainer.links     as L
import numpy             as np

class ActionValue(Chain):
    """
    Decide the next action
    """