from luxembourg     import Board, Line, Point
from luxembourg.dqn import DQN

import copy
import pickle
import numpy             as np

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
        self.dqn = DQN()
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
        state_ = np.asanyarray(self.state.reshape(1, 1, DQN.BOARD_SIZE, DQN.BOARD_SIZE), dtype=np.float32)

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
        state_ = np.asanyarray(self.state.reshape(1, 1, DQN.BOARD_SIZE, DQN.BOARD_SIZE), dtype=np.float32)

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