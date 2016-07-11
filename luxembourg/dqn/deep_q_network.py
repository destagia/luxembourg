from chainer import cuda, Function, Variable, optimizers, serializers

import copy
import pickle
import numpy             as np
import chainer.functions as F

from luxembourg.dqn import ActionValue, ReplayBuffer

class DQN:

    # Hyper-Parameters
    GAMMA                      = 0.99     # Discount factor
    INITIAL_EXPLORATION        = 10 ** 3  # Initial exploratoin. original: 5x10^4
    REPLAY_SIZE                = 32       # Replay (batch) size
    TARGET_MODEL_UPDATE_FREQ   = 10 ** 4  # Target update frequancy. original: 10^4
    DATA_SIZE                  = 10 ** 5  # Data size of history. original: 10^6
    BOARD_SIZE                 = 5

    def __init__(self):
        """
        :param n_act: the number of actions, depending on which AI decides what to do
        """
        self.__step = 0
        self.__n_act = 75

        self.__model = ActionValue(self.__n_act)
        self.__model_target = copy.deepcopy(self.__model)

        self.__optimizer = optimizers.RMSpropGraves(lr=0.00025, alpha=0.95, momentum=0.95, eps=0.01)
        self.__optimizer.setup(self.__model)

        self.__replay_buffer = ReplayBuffer(
            np.zeros((DQN.DATA_SIZE, DQN.BOARD_SIZE, DQN.BOARD_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE, 1), dtype=np.float32),
            np.zeros((DQN.DATA_SIZE, DQN.BOARD_SIZE, DQN.BOARD_SIZE), dtype=np.uint8),
            np.zeros((DQN.DATA_SIZE, 1), dtype=np.bool))

    def get_step(self):
        return self.__step

    def get_model(self):
        return self.__model

    def get_target_model(self):
        return self.__model_target    

    def get_loss(self, state, action, reward, state_prime, episode_end):
        """
        Calculate loss by state, action, reward, next state
        """
        s = Variable(state)
        s_dash = Variable(state_prime.astype(np.float32)) # ???

        # Get Q-value
        q = self.__model.q_function(s)

        # Generate Target Signals
        tmp = self.__model_target.q_function(s_dash)
        tmp = list(map(np.max, tmp.data))
        max_q_prime = np.asanyarray(tmp, dtype=np.float32)
        target = np.asanyarray(copy.deepcopy(q.data), dtype=np.float32)

        for i in range(DQN.REPLAY_SIZE):
            if episode_end[i][0]:
                _tmp = np.sign(reward[i])
            else:
                _tmp = np.sign(reward[i]) + DQN.GAMMA * max_q_prime[i]

            target[i, action[i]] = _tmp

        td = Variable(target) - q
        td_tmp = td.data + 1000.0 * (abs(td.data) <= 1)
        td_clip = td * (abs(td.data) <= 1) + td / abs(td_tmp) * (abs(td.data) > 1)

        zero_val = Variable(np.zeros((DQN.REPLAY_SIZE, self.__n_act), dtype=np.float32))
        loss = F.mean_squared_error(td_clip, zero_val)
        return loss, q

    def stock_experience(self, time, state, action, reward, state_prime, episode_end_flag):
        data_index = time % DQN.DATA_SIZE
        if episode_end_flag:
            state_prime = 0
        else:
            self.__replay_buffer.set(data_index, state, action ,reward, state_prime, episode_end_flag)

    def experience_replay(self, time):
        """
        Experience Replay
        """

        # experience replay is executed only if time pasted enough time
        if DQN.INITIAL_EXPLORATION < time:
            if time < DQN.DATA_SIZE:
                replay_index = np.random.randint(0, time, (DQN.REPLAY_SIZE, 1))
            else:
                replay_index = np.random.randint(0, DQN.DATA_SIZE, (DQN.REPLAY_SIZE, 1))
            s_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1, DQN.BOARD_SIZE, DQN.BOARD_SIZE), dtype=np.float32)
            a_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.int8)
            r_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.float32)
            s_prime_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1, DQN.BOARD_SIZE, DQN.BOARD_SIZE))
            episode_end_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.bool)
            for i in range(self.REPLAY_SIZE):
                index = replay_index[i]
                s_replay[i] = np.asarray(self.__replay_buffer.get_state(index), dtype=np.float32)
                a_replay[i] = self.__replay_buffer.get_action(index)
                r_replay[i] = self.__replay_buffer.get_reward(index)
                s_prime_replay[i] = np.array(self.__replay_buffer.get_state_prime(index), dtype=np.float32)
                episode_end_replay[i] = self.__replay_buffer.get_episode_end_flag(index)

            self.__optimizer.zero_grads()
            loss, _ = self.get_loss(s_replay, a_replay, r_replay, s_prime_replay, episode_end_replay)
            loss.backward()
            self.__optimizer.update()

    def action_sample_e_greedy(self, state, epsilon):
        s = Variable(state)
        q = self.__model.q_function(s)
        q = q.data[0]

        if np.random.rand() < epsilon:
            action = np.random.randint(0, self.__n_act)
            # print("RANDOM : " + str(action))
        else:
            a = np.argmax(q) # a is index of the max value element
            print("GREEDY : " + str(a))
            action = np.asarray(a, dtype=np.int8)
            print(q)

        return action, q

    def target_model_update(self, soft_update):
        if soft_update:
            tau = self.target_update_rate

            model_params = dict(self.model.namedparams())
            model_target_params = dict(self.model_target.namedparams())
            for name in model_target_params:
                model_target_params[name].data = tau * model_params[name].data + (1 - tau) * model_target_params[name].data
        elif np.mod(self.__step, DQN.TARGET_MODEL_UPDATE_FREQ) == 0:
            self.model_target = copy.deepcopy(self.__model)

    def learn(self, state, action, reward, state_prime, terminal):
        self.stock_experience(self.__step, state, action, reward, state_prime, terminal)
        self.experience_replay(self.__step)
        self.target_model_update(soft_update=False)
        self.__step += 1