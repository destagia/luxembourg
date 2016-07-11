from chainer import cuda, Function, Variable, optimizers, serializers
from chainer import Chain
import chainer.functions as F
import chainer.links     as L
import numpy             as np

from luxembourg.dqn import ActionValue

class CNN(Chain):
    def __init__(self):
        super(CNN, self).__init__(
            l1 = F.Convolution2D(1, 32, 3, pad=1),
            l2 = F.Convolution2D(32, 64, 3, pad=1),
            l3 = F.Convolution2D(64, 128, 3, pad=1),
            l4 = F.Linear(3200, 8))

    def eval(self, data):
        h1 = F.relu(self.l1(data))
        h2 = F.relu(self.l2(h1))
        h3 = F.relu(self.l3(h2))
        return self.l4(h3)

data = [[0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1]]

print(data)

data = np.asarray(data).astype(np.float32)
print(data)

data = data.reshape(1, 1, 5, 5)
print(data)

data = Variable(data)

cnn = CNN()
print(cnn.eval(data).data)

actionValue = ActionValue(75)
print(actionValue.q_function(data).data)