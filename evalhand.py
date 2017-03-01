import pandas as pd

rankvalues = dict((r, i)
                  for i, r in enumerate('..23456789TJQKA'))

def eval_hand(hand):


    hand = hand.split()

    suits = [s for r, s in hand]
    ranks = sorted([rankvalues[r] for r, s in hand])
    ranks.reverse()
    flush = len(set(suits)) == 1
    straight = (max(ranks) - min(ranks)) == 4 and len(set(ranks)) == 5

    def kind(n, butnot=None):
        return [r for r in ranks if ranks.count(r) == n and r != butnot]

    if straight and flush: return 9000 + max(ranks)
    if kind(4):            return 8000 + kind(4)[0]
    if kind(3) and kind(2):return 7000 + 50*kind(3)[0] + kind(2)[0]
    if flush:              return 6000 + sum(ranks)
    if straight:           return 5000 + max(ranks)
    if kind(3):            return 4000 + 50*kind(3)[0] + 20*ranks[0] + ranks[1]
    if kind(2) and kind(2, kind(2)[0]): return 3000 + 50*kind(2)[0] + 20*kind(2, kind(2)[0])[0] + max(ranks)
    if kind(2):            return 2000 + 50*kind(2)[0] + sum(ranks[0:4])
    return 1000 + sum(ranks)
