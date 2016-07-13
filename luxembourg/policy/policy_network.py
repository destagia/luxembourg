from luxembourg.policy import PolicyFunction
from chainer import Variable, cuda, Function, Variable, optimizers, serializers
import chainer.functions as F
import numpy as np
import random
import copy

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
        # print("Probabilities")
        # print(probabilities.data[0])
        cursor = random.uniform(0, sum(probabilities.data[0]))

        prob_sum = 0.0
        # print(str(cursor) + " in " + str(sum(probabilities.data[0])))
        for i, val in enumerate(probabilities.data[0]):
            if prob_sum <= cursor and cursor < (prob_sum + val):
                action = i
            prob_sum += val

        return action, probabilities

    def learn_with_diff(self, probabilities, action):
        y = probabilities
        self.__optimizer.update(LoseLossFunction(), y, action)

    def learn_with_cross_entropy(self, probabilities, action):
        y = probabilities
        self.__optimizer.update(WonLossFunction(), y, action)

class WonLossFunction():
    def __call__(self, y, action):
        t = Variable(np.asarray([action]).astype(np.int32))
        return -F.softmax_cross_entropy(y, t)

class LoseLossFunction():
    def __call__(self, y, action):
        t = Variable(np.asarray([action]).astype(np.int32))
        result = F.sum(F.select_item(F.log(F.softmax(y)), t)) / len(y.data)
        # print("loss" + str(result.data))
        return result

