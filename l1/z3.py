from collections import namedtuple
from collections import Counter
import random 

Card = namedtuple('Card', ['rank', 'color'])

class PokerCards:
    def __init__(self, cards_list):
        self.cards_list = cards_list

    def ranks(self):
        return map(lambda x: x.rank, self.cards_list)

    def colors(self):
        return map(lambda x: x.color, self.cards_list)

class PokerRankComparer:
    def is_one_pair(self, cards):
        return len(set(cards.ranks())) < len(cards.ranks())
        
    def is_two_pair(self, cards):
        return len(set(cards.ranks())) + 1 < len(cards.ranks())

    def is_three_of_kind(self, cards):
        return any([x[1] >= 3 for x in Counter(cards.ranks()).iteritems()])

    def is_straight(self, cards):
        sorted_ranks = sorted(cards.ranks())
        return sorted_ranks[0] + 4 == sorted_ranks[-1] and self.is_one_pair(cards) == False

    def is_flush(self, cards):
        return len(set(cards.colors())) == 1

    def is_full_house(self, cards):
        cards_counter = Counter(cards.ranks())
        return len(cards_counter) == 2 and all([x[1] < 4 for x in cards_counter.iteritems()])

    def is_four_of_kind(self, cards):
        return any(x[1] >= 4 for x in Counter(cards.ranks()).iteritems())

    def is_straight_flush(self, cards):
        return self.is_straight(cards) and self.is_flush(cards)

    def is_fig_higher_than_blot(self, fig_cards, blot_cards):
        func_list = [
            self.is_straight_flush, self.is_four_of_kind, self.is_full_house, self.is_flush, 
            self.is_straight, self.is_three_of_kind, self.is_two_pair, self.is_one_pair
        ]
        for func in func_list:
            fig_result = func(fig_cards)
            blot_result = func(blot_cards)
            if fig_result and blot_result == False:
                return True
            elif fig_result == False and blot_result:
                return False
        return True

def draw_poker_cards(deck):
    return PokerCards(random.sample(deck, 5))

def get_blot_win_pbp(fig_deck, blot_deck, draw_count=10000):
    win_count = 0
    rank_comparer = PokerRankComparer()
    for _ in range(draw_count):
        fig_cards = draw_poker_cards(fig_deck)
        blot_cards = draw_poker_cards(blot_deck)
        if rank_comparer.is_fig_higher_than_blot(fig_cards, blot_cards) == False:
            win_count += 1
    return float(win_count) / draw_count
        
def get_fig_full_deck():
    deck = []
    for rank in range(11, 15):
        for color in range(0, 4):
            deck.append(Card(rank, color))
    return deck

def get_blot_full_deck():
    deck = []
    for rank in range(2, 11):
        for color in range(0, 4):
            deck.append(Card(rank, color))
    return deck

def get_blot_half_deck():
    deck = []
    for rank in range(6, 11):
        for color in range(0, 4):
            deck.append(Card(rank, color))
    return deck

def get_blot_color_deck():
    deck = [] 
    for rank in range(2, 11):
        deck.append(Card(rank, 0))
    return deck

def get_blot_win_deck():
    deck = []
    for rank in range(2, 7):
        deck.append(Card(rank, 0))
    return deck

blot_func = (lambda x: get_blot_win_pbp(get_fig_full_deck(), x))
print("Pbp for full deck: %.2f" % blot_func(get_blot_full_deck()))
print("Pbp for half deck: %.2f" % blot_func(get_blot_half_deck()))
print("Pbp for color deck: %.2f" %  blot_func(get_blot_color_deck()))
print("Pbp for win deck: %.2f" % blot_func(get_blot_win_deck()))


