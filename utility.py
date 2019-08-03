from enum import *

''' Defines player move. '''
class Action(Enum):
    HIT = 1
    STICK = 2

''' Defines game state. '''
class State(IntEnum):
    UNRESOLVED = 2
    WIN = 1
    LOST = -1
    DRAW = 0

class Card:
    def __init__(self, label):
        self.label = label

    def value(self):
        if 1 <= self.label <= 10:
            return self.label
        return 10

    def __hash__(self):
        return self.label

    def __eq__(self, card):
        return self.label == card.label

class Ace(Card):
    def __init__(self):
        Card.__init__(self, 1)

class Jack(Card):
    def __init__(self):
        Card.__init__(self, 11)

class Queen(Card):
    def __init__(self):
        Card.__init__(self, 12)

class King(Card):
    def __init__(self):
        Card.__init__(self, 13)
        
class NumericCard(Card):
    def __init__(self, value):
        Card.__init__(self, value)