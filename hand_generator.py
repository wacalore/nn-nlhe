import numpy as np
import matplotlib.pyplot as mp
import itertools
from evalhand import eval_hand

def flatten(iter):
    return list(itertools.chain.from_iterable(iter))

cards = '23456789TJQKA'
suits = 'AHDC'
deck = [x+y for x in cards for y in suits]


def gen_deck(hero_hand):
    hero_hand = hero_hand.split()

    remaining_deck = [j for j in deck if j != hero_hand[0] and j != hero_hand[1]]

    return remaining_deck


def simulate_hand(hero_hand, villains, sims):

    remaining_deck = gen_deck(hero_hand)
    hero_hand = hero_hand.split()
    output = []
    rankings = []

    for k in range(sims):
        shuffled_deck = np.random.permutation(remaining_deck)

        hole_cards = shuffled_deck[0:2*villains]
        hole_cards = hole_cards.reshape(villains, 2)

        offset = 2*villains
        flop = shuffled_deck[offset:(offset+3)]
        turn = shuffled_deck[offset+3]
        river = shuffled_deck[offset+4]

        hero_board_hand = hero_hand + flop.tolist()
        hero_board_hand.append(turn)
        hero_board_hand.append(river)
        hero_board_hand = ' '.join(hero_board_hand)

        hero_score = eval_hand(hero_board_hand)

        results = range(villains)
        for l in range(villains):
            villain_hand = hole_cards[l].tolist() + flop.tolist()
            villain_hand.append(turn)
            villain_hand.append(river)
            villain_hand = ' '.join(villain_hand)
            results[l] = eval_hand(villain_hand)

        output.append(1 if hero_score > max(results) else 0)
        results.append(hero_score)
        rankings.append(sorted(results, reverse=True).index(hero_score))

    return output, rankings

if __name__ == "__main__":

    hand = "JC TC"
    output, rankings = simulate_hand(hand, 4, 10000)
    print np.mean(output)
    print np.mean(rankings)
    mp.hist(rankings)
    mp.show()