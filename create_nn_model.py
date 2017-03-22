# File to sketch NN and inputs/outputs

# Inputs
# 1. Current hand
# 2. Number of other players
# 3. Stack size
# 4. Opponent stack size
# 5. Pot size
# 6. Opponent betting behavior - some kind of parameter to signal if one person is betting big vs everyone else.
# 7. Where in game - pre-flop/flop/turn/river

# Output
# 1. Estimated probability of winning
# 2. Should bet / how much to bet / should call vs raise / etc
# 	a. Need to encode some kind of smart behavior here because if always bets what thinks the pot is worth, it'll tell
# 	all players its hand basically. My guess is the random nature of NNs would incorporate a certain degree of noise on
#	its own. Potentially anchor bets to call - my guess is if a player is throwing random bets (which basically
# 	signals to everyone else its a bot, people may leave).

import tensorflow as tf

from nlhemodel import SimulatedPlayer, NLHEHand

# simple start - two players heads up.

SMALL_BLIND = 50
BIG_BLIND = 100

p1 = SimulatedPlayer()
p2 = SimulatedPlayer()

ffn = tf.contrib.learn.DNNRegressor()
for j in range(100): # 100 simulated hands

	hand = NLHEHand([p1, p2])
	p1.cards = hand.player_cards[p1.nn_id]
	p2.cards = hand.player_cards[p2.nn_id]

	hand.score_hands()

	winner = max(hand.results, key=hand.results.get) # returns id






