'''

    JT should return all 16 combos of JT
    97o should return all 12 combos of off-suit 9 & 7
    AKs should return all 4 combos of suited AK
    15% should return the top 15% of hands
    15-30% should return the top 30-15% of hands

'''

from deck import Deck
import pyparsing as pp
import itertools


rankvalues = dict((r, i)
                  for i, r in enumerate('..23456789TJQKA'))

class RangeBuilder:

    range = []

    def __init__(self):
        return

    def __get__(self):
        return self.range

    def definerange(self, rangestring):

        return


def parse_range(userinput):

    hand_range = []
    if len(userinput) > 1:
        tokens = userinput.split()
    deck = Deck()

    for token in tokens:

        suited = False
        offsuit = False
        ascending = False

        if 's' in token:
            suited = True
            token = token[0:-1]
        elif 'o' in token:
            offsuit = True
            token = token[0:-1]
        elif '+' in token:
            ascending = True
            token = token[0:-1]
            asc_rank = token[-1]
        else:
            pass

        cards = deck.slice_deck(token)
        rank = list(token)
        card_set1 = deck.slice_deck(rank[0])
        card_set2 = deck.slice_deck(rank[1])
        all_combos = list(itertools.product(card_set1, card_set2))

        if suited:
            suited_combos = [(x, y) for x, y in all_combos if x[1] == y[1]]
            hand_range += suited_combos
        elif offsuit:
            offsuit_combos = [(x, y) for x, y in all_combos if x[1] != y[1]]
            hand_range += offsuit_combos
        elif ascending:
            hand_range += all_combos
            ascending_ranks = [x for x in rankvalues if rankvalues[asc_rank] > rankvalues[x] < rankvalues[rank[0]]]
            for card in ascending_ranks:
                asc_cards = deck.slice_deck(card)
                hand_range += list(itertools.product(card_set1, asc_cards))
        else:
            hand_range += all_combos


    '''
    lower_bound = pp.Word(pp.nums).setResultsName('Lower')
    upper_bound = pp.Word(pp.nums).setResultsName('Upper')
    perc_range_pattern = lower_bound + "-" + upper_bound + "%"

    offsuit_pattern = pp.Word(pp.alphas + 'o')
    suited_pattern = pp.Word(pp.alphas + 's')

    '''

    return hand_range




