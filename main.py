import blackjack
import optimalDeterministicPlayer
import utility
import mcExploringStates
import mcEpsilonGreedy
import sarsa
import qLearning

import argparse
import sys

parser = argparse.ArgumentParser(description= 'Blackjack RL')
parser.add_argument('-a', '--algorithm', type=str, help = 'algorithm used to train agent. One of: "Deterministic, MCExploringStates, MCEpsilonGreedy, Sarsa, QLearning "') 
parser.add_argument('--epsilon', type=float, default = 0.1, help = 'epsilon used for probability in e-greedy algorithms, default=0.1')
parser.add_argument('--alpha', type = float, default = 0.01, help = 'alpha used in TD algorithms, default=0.01')
parser.add_argument('--gamma', type = float, default = 0.15, help = 'gamma used in TD algorithms, default=0.15')
parser.add_argument('-e', '--episodes', type=int, default = 100000, help='number of episodes used for learning agent, default=100000')
parser.add_argument('-g', '--games', type=int, default=100000, help='number of games to test agent, default=100000')
args = parser.parse_args()

bj = blackjack.Blackjack()
environment = bj.get_environment()

win_counter = 0
draw_counter = 0
number_of_games = args.games
episodes = args.episodes
epsilon = args.epsilon
alpha = args.alpha
gamma = args.gamma
algorithm = args.algorithm
if algorithm == 'MCExploringStates':
    player = mcExploringStates.MCExploringStatesAgent(environment, episodes)
elif algorithm == 'MCEpsilonGreedy':
    player = mcEpsilonGreedy.MCEpsilonGreedyAgent(environment, episodes, epsilon)
elif algorithm == 'Sarsa':
    player = sarsa.SarsaAgent(environment, episodes, gamma, alpha, epsilon)
elif algorithm == 'QLearning':
    player = qLearning.QLearningAgent(environment, episodes, gamma , alpha , epsilon)
elif algorithm == 'Deterministic':
    player = optimalDeterministicPlayer.OptimalDeterministicPlayer(environment)
else:
    parser.print_help()
    sys.exit()

for _ in range(number_of_games):
    game = bj.new_game(player)
    state = game.play()
    if state == utility.State.WIN:
        win_counter += 1
    if state == utility.State.DRAW:
        draw_counter += 1

print ('Percent of wins:', round(win_counter/number_of_games * 100,2),"%")
print ('Percent of draws:', round(draw_counter/number_of_games * 100,2),"%")