from luxembourg.policy import PolicyFunction
from chainer import Variable, cuda, Function, Variable, optimizers, serializers
import chainer.functions as F
import numpy as np
import random

class PolicyNetwork:

    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.__function = PolicyFunction(input_size, output_size)
        self.__optimizer = optimizers.Adam()
        self.__optimizer.setup(self.__function)

    def get_action(self, raw_state):
        state = np.asarray(raw_state)
        state = state.astype(np.float32)
        state = state.reshape(1, self.input_size)
        state = Variable(state)

        probabilities = self.__function(state)
        print("Probabilities")
        print(probabilities.data[0])
        cursor = random.uniform(0, sum(probabilities.data[0]))

        prob_sum = 0.0
        print(str(cursor) + " in " + str(sum(probabilities.data[0])))
        for i, val in enumerate(probabilities.data[0]):
            if prob_sum <= cursor and cursor < (prob_sum + val):
                action = i
            prob_sum += val

        return action, probabilities


    def learn(self, probabilities, true_data):
        x = probabilities
        t = Variable(np.asarray(true_data).astype(np.int32))
        self.__optimizer.update(F.softmax_cross_entropy, x, t)

class PolicyLossFunction:
    def __call__(self, x, t):
        loss = Variable(np.abs(t.data - x.data))
        # print("loss 1")
        # print(loss.data)
        return loss
