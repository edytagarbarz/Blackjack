from agent import *
import statistics
class MCEpsilonGreedyAgent(Agent):

    def __init__(self, environment, number_of_episodes, epsilon):
        self.number_of_episodes = number_of_episodes
        self.probability = 1 - epsilon + epsilon/2
        Agent.__init__(self, environment)

    def train(self):
        self.counter = 0
        self.returns = dict()
        for state in self.states:
            self.returns[(state, Action.HIT)] = list()
            self.returns[(state, Action.STICK)] = list()
        for k in range(self.number_of_episodes):
            state0, action0 = self.get_random_state_action_pair()
            episode = self.generate_episode(state0, action0)
            states = set()
            _, _, game_state = episode[-1]
            reward = game_state
            for (state, action, _) in episode:
                self.returns[(state, action)].append(reward)
                self.action_value_function[(state, action)] = statistics.mean(self.returns[(state, action)])
                states.add(state)
            self.get_policy_from_action_value_function(states, self.probability)
        