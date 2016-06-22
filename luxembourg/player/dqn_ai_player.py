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

class ReplayBuffer:
    def __init__(self, states, actions, rewards, state_primes, episode_end_flags):
        self.__states = states
        self.__actions = actions
        self.__rewards = rewards
        self.__state_primes = state_primes
        self.__episode_end_flags = episode_end_flags

    def set(self, index, state, action, reward, state_prime, episode_end_flag):
        self.__states[index] = state
        self.__actions[index] = action
        self.__rewards[index] = reward
        self.__state_primes[index] = state_prime
        self.__episode_end_flags[index] = episode_end_flag

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
    INITIAL_EXPLORATION        = 10 ** 3  # Initial exploratoin. original: 5x10^4
    REPLAY_SIZE                = 32       # Replay (batch) size
    TARGET_MODEL_UPDATE_FREQ   = 10 ** 4  # Target update frequancy. original: 10^4
    DATA_SIZE                  = 10 ** 5  # Data size of history. original: 10^6
    BOARD_SIZE                 = 5

    def __init__(self, n_act):
        """
        :param n_act: the number of actions, depending on which AI decides what to do
        """
        self.__step = 0
        self.__n_act = n_act

        self.__model = ActionValue(n_act)
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
        print(state)
        s = Variable(state)
        s_dash = Variable(state_prime)

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

        zero_val = Variable(np.zeros((DQN.REPLAY_SIZE, self.n_act), dtype=np.float32))
        loss = F.mean_squared_error(td_clip, zero_val)
        return loss, q

    def stock_experience(self, time, state, action, reward, state_prime, episode_end_flag):
        data_index = time % DQN.DATA_SIZE
        if episode_end_flag:
            state_prime = 0
        else:
            self.__replay_buffer.set(data_index, state, action ,reward, state_prime, episode_end_flag)

    def experience_replay(self, time):
        if DQN.INITIAL_EXPLORATION < time:
            if time < DQN.DATA_SIZE:
                replay_index = np.random.randint(0, time, (DQN.REPLAY_SIZE, 1))
            else:
                replay_index = np.random.randint(0, DQN.DATA_SIZE, (DQN.REPLAY_SIZE, 1))
            s_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, DQN.BOARD_SIZE, DQN.BOARD_SIZE, 1, 1), dtype=np.float32)
            a_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.int8)
            r_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.float32)
            s_prime_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, DQN.BOARD_SIZE, DQN.BOARD_SIZE, 1, 1))
            episode_end_replay = np.ndarray(shape=(DQN.REPLAY_SIZE, 1), dtype=np.bool)
            for i in range(self.REPLAY_SIZE):
                index = replay_index[i]
                s_replay[i] = np.asarray(self.__replay_buffer.get_states()[index], dtype=np.float32)
                a_replay[i] = self.__replay_buffer.get_actions()[index]
                r_replay[i] = self.__replay_buffer.get_rewards()[index]
                s_prime_replay[i] = np.array(self.__replay_buffer.get_state_primes()[index], dtype=np.float32)
                episode_end_replay[i] = self.__replay_buffer.get_episode_end_flags()[index]

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

class DqnAiPlayer:
    """
    AI created with DQN (Deep Q-Network)
    In the context of DQN, this is what so called Agent
    """

    def __init__(self, board, symbol):
        points = [Point(x, y) for x in range(0, 5) for y in range(0, 5) if x >= y]
        def distinct(acc, x):
            if not x in acc:
                acc.append(x)
            return acc
        def validate(acc, points):
            p1, p2 = points
            x_diff = p1.get_x() - p2.get_x()
            y_diff = p1.get_y() - p2.get_y()
            if x_diff == 0 or y_diff == 0 or x_diff == y_diff:
                if p2.get_x() < p1.get_x() or p2.get_y() < p1.get_y():
                    points = (p2, p1)
                acc.append(Line(points[0], points[1]))
            return acc
        lines = reduce(distinct, [set([x, y]) for x in range(0, 15) for y in range(0, 15)], [])
        lines = map(lambda x: list(x) + list(x) if len(x) == 1 else sorted(list(x)), lines)
        lines = map(lambda x: (points[x[0]], points[x[1]]), lines)
        lines = reduce(validate, lines, [])
        self.lines = lines
        self.epsilon = 1.0
        self.dqn = DQN(n_act=75)
        self.__symbol = symbol
        self.__board  = board
        self.__policyFrozen = False
        self.__current_reward = 0.0
        self.__total_score = 0.0

    def set_current_reward(self, reward):
        self.__current_reward = reward
        self.__total_score += reward

    def get_current_reward(self):
        return self.__current_reward

    def reset(self, board):
        self.__episode = 0
        self.__board = board

    def get_line(self):
        self.__episode = self.__episode or 0

        # If count equals 1 before drwaing line,
        # It means that AI LOST!
        if self.__board.get_none_count() == 1:
            self.set_current_reward(-0.5)
            self.end(self.get_current_reward())

            last_point = self.__board.get_empty_points()[0]
            return Line(last_point, last_point)

        state = self.__board.get_as_array()
        while True:
            if self.__episode == 0:
                action = self.start(state)
            else:
                action = self.act(state, self.get_current_reward())

            selected_line = self.lines[action]
            stub_board = Board(board=self.__board)
            try:
                stub_board.draw_line(self, selected_line)
            except:
                continue
            break


        point_count = stub_board.get_none_count()
        if point_count == 1:
            self.set_current_reward(1)
        elif point_count == 0:
            self.set_current_reward(-0.5)
        else:
            self.set_current_reward(0)

        self.__episode += 1
        return selected_line

    def get_symbol(self):
        return self.__symbol

    def start(self, observation):
        """
        Will be invoked at first episode
        The reason why start and act are separated is just that
        First step does not have the reward
        """
        self.reset_state(observation)
        state_ = np.asanyarray(self.state.reshape(DQN.BOARD_SIZE, DQN.BOARD_SIZE, 1, 1), dtype=np.float32)

        # Generate an Action e-greedy
        action, Q_now = self.dqn.action_sample_e_greedy(state_, self.epsilon)

        # Update for next step
        self.last_action = action
        self.last_state = copy.deepcopy(self.state)

        return action

    def act(self, observation, reward):
        """
        After start step, this method will be called consistently
        """
        self.set_state(observation)
        state_ = np.asanyarray(self.state.reshape(DQN.BOARD_SIZE, DQN.BOARD_SIZE, 1, 1), dtype=np.float32)

        # Exploration decays along the time sequence
        if self.__policyFrozen is False:  # Learning ON/OFF
            if DQN.INITIAL_EXPLORATION < self.dqn.get_step():
                self.epsilon -= 1.0 / 10**6
                if self.epsilon < 0.1:
                    self.epsilon = 0.1
                eps = self.epsilon
            else:
                # Initial Exploation Phase
                # print("Initial Exploration : %d/%d steps" % (self.dqn.get_step(), DQN.INITIAL_EXPLORATION))
                eps = 1.0
        else:  # Evaluation
                # print("Policy is Frozen")
                eps = 0.05

        # Generate an Action by e-greedy action selection
        action, Q_now = self.dqn.action_sample_e_greedy(state_, eps)

        # Learning Phase
        if self.__policyFrozen is False:  # Learning ON/OFF
            self.dqn.learn(self.last_state, self.last_action, reward, self.state, False)
            self.last_action = copy.deepcopy(action)
            self.last_state = self.state.copy()

        # Simple text based visualization
        # print(' Time Step %d /   ACTION  %d  /   REWARD %.1f   / EPSILON  %.6f  /   Q_max  %3f' % (self.dqn.get_step(), action, np.sign(reward), eps, np.max(Q_now)))

        return action

    def end(self, reward):  # Episode Terminated

        # Learning Phase
        if self.__policyFrozen is False:  # Learning ON/OFF
            self.dqn.learn(self.last_state, self.last_action, reward, self.last_state, True)

        # Simple text based visualization
        # print('  REWARD %.1f   / EPSILON  %.5f' % (np.sign(reward), self.epsilon))


    def reset_state(self, obs_array):
        obs_array = np.asarray(obs_array)
        # Updates for next step
        self.last_observation = obs_array

        # Initialize State
        self.state = obs_array

    def set_state(self, obs_array):
        obs_array = np.asarray(obs_array)
        obs_processed = np.maximum(obs_array, self.last_observation)  # Take maximum from two frames
        # Updates for the next step
        self.last_observation = obs_array

        self.state = obs_processed.astype(np.uint8)

    def save(self):
        serializers.save_npz('network/model.model',        self.dqn.get_model())
        serializers.save_npz('network/model_target.model', self.dqn.get_target_model())
        print("------------ Networks were SAVED ---------------")