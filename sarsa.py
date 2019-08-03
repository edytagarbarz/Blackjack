from agent import *
import statistics

class SarsaAgent(Agent):

    def __init__(self, environment, number_of_episodes, gamma, alpha, epsilon):
        self.gamma = gamma
        self.number_of_episodes = number_of_episodes
        self.probability = 1 - epsilon + epsilon/2
        self.alpha = alpha
        Agent.__init__(self, environment)

    def get_epsilon_greedy_action(self, state):
        if state not in self.states:
            return Action.STICK
        betterAction = Action.HIT
        worseAction = Action.STICK
        if self.action_value_function[(state, Action.STICK)] > self.action_value_function[(state, Action.HIT)]:
            betterAction = Action.STICK
            worseAction = Action.HIT
        probability = random.random()
        if probability < self.probability:
            action = betterAction
        else:
            action = worseAction
        return action

    def train(self):
        for k in range(self.number_of_episodes):
            S = self.get_random_state()
            A = self.get_epsilon_greedy_action(S)
            while(True):
                nextS, reward = self.environment.agent_learn_step(S, A)
                if reward == State.UNRESOLVED:
                    reward = 0
                nextA = self.get_epsilon_greedy_action(nextS)
                currentVal = self.action_value_function[(S,A)]
                if nextS not in self.states: 
                    nextVal = 0
                else :
                    nextVal = self.action_value_function[(nextS, nextA)]
                self.action_value_function[(S,A)] = currentVal + self.alpha * (reward + self.gamma * nextVal - currentVal)
                S = nextS
                A = nextA
                if reward != State.UNRESOLVED:
                    break
        self.get_policy_from_action_value_function( self.states, self.probability)


            