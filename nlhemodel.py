'''
action_sequence -- represents the sequence of betting actions in the game
	Current format will be for a 2 player (Heads-UP) game
	Format is a sequence of integers [0,1,2,3]
	0 - Not yet reached
	1 - Fold
	2 - Call/Check
	3 - Raise
'''

import string
import random
import numpy as np
import itertools
from evalhand import eval_hand

cards = '23456789TJQKA'
suits = 'SHDC'
FULL_DECK = [x + y for x in cards for y in suits]
DECK_DICT = dict((r, i)
				 for i, r in enumerate(FULL_DECK))


class SimulatedPlayer(object):

	def __init__(self, strategy=None, chips=0.0, nn_id=None):
		self.chips = chips  # some int here
		self.action_sequence = np.zeros(16)
		self.strategy = strategy
		self.nn_id = nn_id

		if not nn_id:
			# pass in NN model to associate with player
			self.nn_id = ''.join(random.sample(string.ascii_uppercase+string.digits, 5))

	def update_chips(self, delta_chips):
		"""
		Call after hand is played to change amount of chips associated with player
		:param delta_chips: amount to increment/decrement chips by
		:return: None - updates object
		"""
		self.chips += delta_chips


class NLHEHand(object):

	IDs = {}

	def __init__(self, list_of_players, blind):
		self.players = list_of_players  # type(list) from SimulatedPlayer class
		self.flop = []
		self.turn = []
		self.river = []
		self.hands = {}
		self.bigblind = blind

		# create shuffled playing deck
		random.shuffle(FULL_DECK)
		self.deck_iter = iter(FULL_DECK)

		# deal cards on init
		self.player_cards = dict(zip(
			[player.nn_id for player in self.players],
			[[next(self.deck_iter), next(self.deck_iter)] for player in self.players]
		))

	def deal_flop(self):
		self.flop = [next(self.deck_iter), next(self.deck_iter), next(self.deck_iter)]
		self.state()

	def deal_turn(self):
		self.turn = [next(self.deck_iter)]
		self.state()

	def deal_river(self):
		self.river = [next(self.deck_iter)]
		self.state()

	def state(self):
		self.hands = dict(zip(
			[player.nn_id for player in self.players],
			[self.player_cards[player.nn_id] + self.flop + self.turn + self.river for player in self.players]))

	def get_ids(self):
		self.IDs = dict((player.nn_id, player) for player in self.players)

	def score_hands(self):
		"""
		Use eval_hand to return winner ID (assume all players finish)
		:return: nn_id
		"""
		self.results = dict(zip(
			self.hands.keys(),
			[eval_hand(" ".join(p_hand)) for p_hand in self.hands.values()]
		))
		return self.results


class HeadsUpRiverAction(NLHEHand):

	def __init__(self, list_of_players, blinds):
		NLHEHand.__init__(self, list_of_players, blinds)
		assert len(list_of_players) == 2

		self.pot = 2*blinds
		[player.update_chips(-1.0*blinds) for player in self.players]
		self.get_ids()

	def hand_to_input(self, player1, player2, previous_action, bet_to_call):
		cards_to_num = [DECK_DICT[x] for x in self.hands[player1.nn_id]]
		player1.action_sequence = [self.pot, player1.chips, player2.chips, previous_action, bet_to_call]
		player1.action_sequence.append(cards_to_num)

	def execute(self):
		self.deal_flop()
		self.deal_turn()
		self.deal_river()

		# Determine which player is next to act
		player_cycle = itertools.cycle(self.players)
		player_to_act = next(player_cycle)
		previous_action = 0.0
		bet_to_call = 0.0

		# Betting action logic
		while True:
			next_player = next(player_cycle)
			self.hand_to_input(player_to_act, next_player, previous_action, bet_to_call)

			action = player_to_act.strategy(player_to_act.action_sequence)
			raise_action = action[0]
			bet_size = action[1]

			rounded = round(raise_action)
			if rounded == 1:
				#Fold
				break

			if rounded == 2:
				#Check
				previous_action = 2

			if rounded == 3:
				#Call
				if previous_action == 4:
					if player_to_act.chips > bet_to_call:
						self.pot += bet_to_call
						player_to_act.chips -= bet_to_call
						break
					else:
						self.pot += player_to_act.chips
						player_to_act.chips = 0.0
						break
				elif previous_action == 2:
					break
				else:
					previous_action = 2
					continue

			if rounded == 4:
				print(self.pot)
				#Raise/bet
				bet_size = min(player_to_act.chips, bet_size)
				if bet_size > bet_to_call:
					bet_to_call = bet_size - bet_to_call
					self.pot += bet_size
					player_to_act.chips -= bet_size
					previous_action = 4
					continue
				else:
					previous_action = 1
					break

			player_to_act = next_player

		#end while
		if previous_action == 1:
			next_player.update_chips(self.pot)

		else:
			results = self.score_hands()
			winner = max(results, key=results.get)
			winning_player = self.IDs[winner]
			winning_player.update_chips(self.pot)


def teststrat(input):
	return [4.0,100.0]


def test_player_hand_classes():
	players = [SimulatedPlayer() for k in range(7)]

	# create a hand
	hand = NLHEHand(list_of_players=players)

if __name__ == "__main__":
	sim1 = SimulatedPlayer(strategy=teststrat,chips=1000, nn_id=1)
	sim2 = SimulatedPlayer(strategy=teststrat,chips=1000, nn_id=2)
	testhand = HeadsUpRiverAction([sim1,sim2], 2.0)

	testhand.execute()
	print(sim1.chips)
	print(sim2.chips)