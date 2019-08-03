# Blackjack
Reinforcement learning algorithms for Blackjack game. Use main.py to train agent, simulate games and print percent of wins and draws.
```bash
usage: main.py [-h] [-a ALGORITHM] [--epsilon EPSILON] [--alpha ALPHA]
               [--gamma GAMMA] [-e EPISODES] [-g GAMES]

Blackjack RL

optional arguments:
  -h, --help            show this help message and exit
  -a ALGORITHM, --algorithm ALGORITHM
                        algorithm used to train agent. One of: "Deterministic, 
                        MCES, MCEpsilonGreedy, Sarsa, QLearning "
  --epsilon EPSILON     epsilon used for probability in e-greedy algorithms,
                        default=0.1
  --alpha ALPHA         alpha used in TD algorithms, default=0.01
  --gamma GAMMA         gamma used in TD algorithms, default=0.15
  -e EPISODES, --episodes EPISODES
                        number of episodes used for learning agent,
                        default=100000
  -g GAMES, --games GAMES
                        number of games to test agent, default=100000
```