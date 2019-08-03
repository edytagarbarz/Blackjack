from blackjack import *
from utility import *

class OptimalDeterministicPlayer(Blackjack.Player):
    def make_move(self):
        points, used_ace = self.environment.count_points(self.get_cards())
        if used_ace:
            if points <= 17 or (points == 18 and self.dealer_card in (NumericCard(9), NumericCard(10), Ace())):
                return self.hit()
            return self.stick()
        if points <= 16 and self.dealer_card in (NumericCard(7), NumericCard(8), NumericCard(9), NumericCard(10)):
            return self.hit()
        if points <= 12 and self.dealer_card in (NumericCard(2), NumericCard(3)):
            return self.hit()
        if points <= 11:
            return self.hit()
        return self.stick()