from agent import *
import statistics

class MCExploringStatesAgent(Agent):
    def __init__(self, environment, number_of_episodes):
        self.number_of_episodes = number_of_episodes
        Agent.__init__(self, environment)
        
    def train(self):
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
            for state in states:
                action = Action.STICK
                if self.action_value_function[(state, Action.HIT)] > self.action_value_function[(state, Action.STICK)]:
                    action = Action.HIT
                self.policy[state] = action

    