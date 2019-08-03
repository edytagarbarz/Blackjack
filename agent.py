from blackjack import *
from utility import *

class Agent(Blackjack.Player):
    
    def __init__(self, environment):
        Blackjack.Player.__init__(self, environment)
        self.init_states()
        self.init_policy()
        self.init_action_value_function()
        self.train()

    def train(self):
        pass

    def init_states(self):
        self.states = list()
        for points in range(10,22):
            for dealer_card in self.environment.tile:
                self.states.append((points, dealer_card, True))
                self.states.append((points, dealer_card, False))
        

    def init_policy(self):
        self.policy = dict()
        for state in self.states:
            points = state[0]
            if points < 20:
                self.policy[state] = Action.HIT
            else:
                self.policy[state] = Action.STICK
            
    def init_action_value_function(self):
        self.action_value_function = dict()
        for state in self.states:
            self.action_value_function[(state, Action.HIT)] = 0
            self.action_value_function[(state, Action.STICK)] = 0

    '''Generates episode based on the current policy'''
    def generate_episode(self, state, action):
        episode = list()
        while True:
            new_state, game_state = self.environment.agent_learn_step(state, action)
            episode.append((state, action, game_state))
            if game_state != State.UNRESOLVED:
                break
            state = new_state
            action = self.policy[state]
        return episode
    

    def get_random_state(self):
        states = len(self.states)
        i = random.randint(0, states - 1)
        return self.states[i]

    def get_random_state_action_pair(self):
        state = self.get_random_state()
        if random.randint(0,1) == 0:
            return (state, Action.HIT)
        else:
            return (state, Action.STICK)

    def get_policy_from_action_value_function(self, states, probability = 1):
        for state in states:
            betterAction = Action.HIT
            worseAction = Action.STICK
            if self.action_value_function[(state, Action.STICK)] > self.action_value_function[(state, Action.HIT)]:
                betterAction = Action.STICK
                worseAction = Action.HIT
            prob = random.random()
            if prob < probability:
                self.policy[state] = betterAction
            else:
                self.policy[state] = worseAction

    ''' Makes move based on the learned policy '''
    def make_move(self):
        points, used_ace = self.environment.count_points(self.get_cards())
        if points < 10:
            return self.hit()
        state = (points, self.dealer_card, used_ace)
        action = self.policy[state]
        if action == Action.HIT:
            return self.hit()
        return self.stick()
        

