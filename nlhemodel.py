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

	def __init__(self, strategy=None, chips=None, nn_id=None):
		self.chips = 0  # some int here
		self.action_sequence = np.zeros(16)
		self.strategy = strategy

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

	IDs = []

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
		for player in self.players:
			self.IDs.append(player.nn_id)

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
		self.get_ids()

	def hand_to_input(self, player1, player2):
		cards_to_num = [DECK_DICT[x] for x in self.hands[player1.nn_id]]
		player1.action_sequence = [self.pot, player1.chips, player2.chips]
		player1.action_sequence.append(cards_to_num)

	def execute(self):
		self.deal_flop()
		self.deal_turn()
		self.deal_river()

		player_cycle = itertools.cycle(self.players)
		player_to_act = next(player_cycle)

		while True:
			next_player = next(player_cycle)
			self.hand_to_input(player_to_act, next_player)



def test_player_hand_classes():
	players = [SimulatedPlayer() for k in range(7)]

	# create a hand
	hand = NLHEHand(list_of_players=players)

