import json
from hand_generator import simulate_hand
from numpy import mean

cards = '23456789TJQKA'
suits = 'SHDC'
deck = [x+y for x in cards for y in suits]

# generate a json file containing results from simulation on all cards

# first generate all possible two card hands

all_poss_hands = [tuple(sorted((card, other_card))) for card in deck for other_card in deck[:deck.index(card)]+deck[deck.index(card)+1:]]
# remove duplicates
all_poss_hands = list(set(all_poss_hands))

# generate outputs from hand_generator and export to json file
output_dict = {}
with open('hand_win_prob_and_ranks.json', 'w') as json_out:
	for hand in all_poss_hands:
		print all_poss_hands.index(hand)
		output, rankings = simulate_hand(' '.join(hand), villains=4, sims=1000)
		output_dict[' '.join(hand)] = {
			'win_prob': mean(output),
			'rankings': mean(rankings)
		}
	json.dump(output_dict, json_out)