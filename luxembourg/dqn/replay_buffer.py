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

    def get_state(self, index):
        """
        State (array replaseting Board)
        """
        return self.__states[index]

    def get_action(self, index):
        """
        Action AI execute
        """
        return self.__actions[index]

    def get_reward(self, index):
        return self.__rewards[index]

    def get_state_prime(self, index):
        return self.__state_primes[index]

    def get_episode_end_flag(self, index):
        return self.__episode_end_flags[index]