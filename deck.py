

cards = '23456789TJQKA'
suits = 'SHDC'
full_deck = [x+y for x in cards for y in suits]


class Deck:

    def __init__(self):
        self.my_deck = full_deck
        self.suits = suits
        self.cards = cards

    def __get__(self):
        return self.my_deck

    def gen_deck(self, hero_hand):
        hero_hand = hero_hand.split()
        remaining_deck = [j for j in full_deck if j != hero_hand[0] and j != hero_hand[1]]
        self.my_deck = remaining_deck

    def slice_deck(self, rank, suits='SHDC'):
        deck_slice = [r+s for r, s in self.my_deck if r in rank and s in suits]
        return deck_slice
