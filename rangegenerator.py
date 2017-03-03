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
    tokens = userinput.split()
    deck = Deck()

    for token in tokens:

        suited = False
        offsuit = False

        if 's' in token:
            suited = True
            token = token[0:-1]
        elif 'o' in token:
            offsuit = True
            token = token[0:-1]
        else:
            pass

        cards = deck.slice_deck(token)

        if suited:
            rank = list(token)
            for suit in deck.suits:
                hand_range.append([rank[0]+suit+rank[1]+suit])
        elif offsuit:
            # TODO deal with offsuit
            pass
        else:
            hand_range.append(list(itertools.combinations(cards, 2)))

    '''
    lower_bound = pp.Word(pp.nums).setResultsName('Lower')
    upper_bound = pp.Word(pp.nums).setResultsName('Upper')
    perc_range_pattern = lower_bound + "-" + upper_bound + "%"

    offsuit_pattern = pp.Word(pp.alphas + 'o')
    suited_pattern = pp.Word(pp.alphas + 's')

    '''

    return hand_range




