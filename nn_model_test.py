import string
import random
from evalhand import eval_hand

cards = '23456789TJQKA'
suits = 'SHDC'
full_deck = [x + y for x in cards for y in suits]

class SimulatedPlayer(object):

	def __init__(self, nn_id=None):
		self.chips = 0  # some int here
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

	def __init__(self, list_of_players):
		self.players = list_of_players  # type(list) from SimulatedPlayer class

		# create shuffled playing deck
		random.shuffle(full_deck)  # shuffle in place
		deck_iter = iter(full_deck)

		# deal cards on init
		self.player_cards = dict(zip(
			[player.nn_id for player in self.players],
			[[next(deck_iter), next(deck_iter)] for player in self.players]
		))
		self.flop = [next(deck_iter), next(deck_iter), next(deck_iter)]
		self.turn = [next(deck_iter)]
		self.river = [next(deck_iter)]

		self.hands_with_community_cards = dict(zip(
			[player.nn_id for player in self.players],
			[self.player_cards[player.nn_id] + self.flop + self.turn + self.river for player in self.players]))

	def score_hands(self):
		"""
		Use eval_hand to return winner ID (assume all players finish)
		:return: nn_id
		"""
		self.results = dict(zip(
			self.hands_with_community_cards.keys(),
			[eval_hand(" ".join(p_hand)) for p_hand in self.hands_with_community_cards.values()]
		))
		return self.results



def test_player_hand_classes():
	players = [SimulatedPlayer() for k in range(7)]

	# create a hand
	hand = NLHEHand(list_of_players=players)


test_player_hand_classes()