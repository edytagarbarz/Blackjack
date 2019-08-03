from utility import *
import random
''' To play a game one need to call new_game(player) 
    with player implementing make_move() method '''
class Blackjack:
    def __init__(self):
        self.environment = Blackjack.Environment()
    def get_environment(self):
        return self.environment
    ''' Given a player returns new game. '''
    def new_game(self, player : 'Blackjack.Player'):
        dealer = Blackjack.Environment.Dealer(self.environment)
        return Blackjack.Game(self.environment, player, dealer)

    class Environment:

        def __init__(self):
            self.tile = [Ace()]
            for i in range (2, 11):
                self.tile.append(NumericCard(i))

        def get_card(self):
            random.shuffle(self.tile)
            return self.tile[0]

        def count_points(self, cards):
            points = 0
            ace = False
            used_ace = False
            for c in cards:
                points += c.value()
                if type(c) == Ace:
                    ace = True
            if ace and points <= 11:
                points += 10
                used_ace = True 
            return points, used_ace

        ''' Given player and dealer cards returns game state after drawing two cards '''
        def after_init_state(self, player_cards, dealer_cards):
            player_points, _ = self.count_points(player_cards)
            dealer_points, _ = self.count_points(dealer_cards)
            if player_points == 21:
                if dealer_points == 21:
                    return State.DRAW
                return State.WIN
            return State.UNRESOLVED

        ''' Given player and dealer cards returns game state at the end of the game'''
        def end_game_state_for_cards(self, player_cards, dealer_cards):
            player_points, _ = self.count_points(player_cards)
            dealer_points, _ = self.count_points(dealer_cards)
            return self.end_game_state(player_points, dealer_points)

        def end_game_state(self, player_points, dealer_points):
            if player_points > 21:
                return State.LOST
            if dealer_points > 21:
                return State.WIN
            if player_points == dealer_points:
                return State.DRAW
            if player_points > dealer_points:
                return State.WIN
            return State.LOST

        ''' Given player cards returns if player exceeded 21 points'''
        def end_player_turn(self, player_cards):
            if self.count_points(player_cards)[0] > 21:
                return True
            return False

        ''' For given state and next action simulates step and returns new state'''
        def agent_learn_step(self, state, action):
            points, dealer_card, used_ace = state
            if action == Action.STICK:
                dealer_points = self.agent_learn_dealer_turn(dealer_card)
                return (state, self.end_game_state(points, dealer_points))
            else:
                card = self.get_card()
                new_points, used_ace = self.agent_learn_count_points(points, used_ace, card)
                if new_points > 21:
                    return ((new_points, dealer_card, used_ace), State.LOST)
                return ((new_points, dealer_card, used_ace), State.UNRESOLVED)

        def agent_learn_dealer_turn(self, card):
            dealer = Blackjack.Environment.Dealer(self)
            dealer.cards.append(card)
            while True:
                move = dealer.make_move()
                if move == Action.STICK:
                    break
            dealer_points, _ =  self.count_points(dealer.get_cards())
            return dealer_points

        def agent_learn_count_points(self, old_points, used_ace, new_card):
            if used_ace:
                old_points -= 10
            old_points += new_card.value()
            if old_points < 12 and used_ace == True:
                old_points += 10
                return (old_points, True)
            return (old_points, False)
    
        class Dealer:
            def __init__(self, environment):
                self.environment = environment
                self.cards = list()

            def init_game(self, cards):
                self.cards.append(cards[0])
                self.cards.append(cards[1])

            def make_move(self):
                points, _ = self.environment.count_points(self.get_cards())
                if  points < 17:
                    self.hit()
                    return Action.HIT
                return Action.STICK

            def hit(self):
                self.cards.append(self.environment.get_card())

            def get_cards(self):
                return list(self.cards)

    class Player:
        def __init__(self, environment):
            self.environment = environment
            self.cards = list()

        ''' Saves first two cards and the revealed dealer's card '''
        def init_game(self, first_card, second_card, dealer_card):
            self.cards.append(first_card)
            self.cards.append(second_card)
            self.dealer_card = dealer_card

        def get_cards(self):
            return list(self.cards)

        def clear_cards(self):
            self.cards.clear()

        def hit(self):
            self.cards.append(self.environment.get_card())
            return Action.HIT

        def stick(self):
            return Action.STICK

        ''' Single move in player's turn. Returns type of the move. '''
        def make_move(self):
            pass

    class Game:
        def __init__(self, environment, player, dealer):
            self.environment = environment
            self.player = player
            self.dealer = dealer

        ''' Returns first two cards for each player and dealer. '''
        def start_game(self):
            self.player.clear_cards()
            player_cards = (self.environment.get_card(), self.environment.get_card())
            dealer_cards = (self.environment.get_card(), self.environment.get_card())
            return (player_cards, dealer_cards)

        ''' Returns if it's the end of the player move. '''
        def end_player_turn(self):
            return self.environment.end_player_turn(self.player.get_cards())
            
        ''' Simulates game. Returns end game state. '''
        def play(self):
            player_cards, dealer_cards = self.start_game()
            self.player.init_game(player_cards[0], player_cards[1], dealer_cards[0])
            self.dealer.init_game(dealer_cards)
            game_state = self.environment.after_init_state(player_cards, dealer_cards)
            if game_state == State.WIN or game_state == State.DRAW:
                return game_state
            while True:
                move = self.player.make_move()
                if move == Action.STICK or self.end_player_turn():
                    break
            while True:
                move = self.dealer.make_move()
                if move == Action.STICK:
                    break
            return self.environment.end_game_state_for_cards(self.player.get_cards(), self.dealer.get_cards())

