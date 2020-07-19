from enum import Enum
from collections import deque
import time
import random

class InvalidCardError(Exception):
    pass

class Card():
    NUMBER_CARD = 0
    WIND_CARD = 1

    NUMS = ["TONG", "TIAO", "WAN"]
    WINDS = ["DONG", "NAN", "XI", "BEI", "FACAI", "ZHONG", "BAN"]

    def __init__(self, card_type, symbol, num=0):
        if (card_type == Card.NUMBER_CARD):
            if num <= 0 or num >= 10:
                raise InvalidCardError("Card number {} out of range".format(num))
            if symbol not in Card.NUMS:
                raise InvalidCardError("Card symbol \"" + symbol + "\" invalid number card symbol")
        elif (card_type == Card.WIND_CARD):
            if symbol not in Card.WINDS:
                raise InvalidCardError("Card symbol \"" + symbol + "\" invalid wind card symbol")
        else:
            raise InvalidCardError("Card type {} invalid. Should be 0 (number) or 1 (wind)".format(card_type))

        self.card_type = card_type # Wind or Number (TODO Flower)
        self.symbol = symbol # Symbol on card
        self.number = num # Nubmer for nubmer card
        self.used = False # If already used in a revealed set

    def __eq__(self, obj):
        return (isinstance(obj, Card)
            and obj.card_type == self.card_type
            and obj.symbol == self.symbol
            and obj.number == self.number)

    def __lt__(self, other):
        assert(isinstance(other, Card))
        if (self.card_type != other.card_type):
            return self.card_type < other.card_type
        if (self.symbol != other.symbol):
            return self.symbol < other.symbol
        return self.number < other.number

    def __str__(self):
        return self.symbol + "_" + str(self.number)

    def __repr__(self):
        return self.__str__()

    def prev_card(self):
        if self.card_type == Card.WIND_CARD:
            return None
        if self.number == 1:
            return None
        return Card(self.card_type, self.symbol, self.number - 1)

    def from_string(card_str):
        split = card_string.split("_")
        symbol = split[0]
        number = int(split[1])
        if (symbol in NUMS):
            return Card(Card.NUMBER_CARD, symbol, number)
        elif (symbol in WINDS):
            return card(Card.WIND_CARD, symbol)
        else:
            raise Exception("Bad string")


def gen_cards():
    cards = []
    for card in Card.NUMS:
        for i in range(4):
            for num in range(1, 10):
                cards.append(Card(Card.NUMBER_CARD, card, num))

    for card in Card.WINDS:
        for i in range(4):
            cards.append(Card(Card.WIND_CARD, card))

    random.shuffle(cards)
    return cards


def check_win(cards):
    # Check a hand of cards is 4 sets + one pair by trying all possible pairs
    def check_normal(cards):
        # Given some set do the rest of the cards form sets?
        # The reason this works for
        def check_sets(cards):
            assert(len(cards) % 3 == 0)
            if (len(cards) == 0): return True

            cards = sorted(cards)
            while (len(cards) != 0):
                cur = cards[-1]
                if (cards.count(cur) == 3):
                    cards = list(filter(lambda c: c != cur, cards))
                else:
                    prev = cur.prev_card()
                    if (prev is None): return False
                    pprev = prev.prev_card()
                    if prev not in cards or pprev not in cards: return False
                    cards.remove(cur)
                    cards.remove(prev)
                    cards.remove(pprev)

            return True

        # check all sets are good
        revealed = list(filter(lambda c : c.used, cards))
        assert(check_sets(revealed))

        # remove all revealed card
        cards = filter(lambda c : not c.used, cards)
        cards = sorted(cards)
        last_check = None
        for i in range(len(cards) - 1):
            if (cards[i] == cards[i + 1] and last_check != cards[i]):
                if (check_sets(cards[:i] + cards[i+2:])):
                    return True
                last_check = cards[i]

        return False

    # Check there are 7 pairs
    def check_7_pairs(cards):
        assert(len(cards) == 14)
        cards = cards.copy()
        while len(cards) != 0:
            c1 = cards.pop()
            c2 = cards.pop()
            if (c1.used or c2.used):
                return False

            if c1 != c2:
                return False
        return True

    if (len(cards) != 14):
        return False

    # TODO: apply point values?
    win_conditions = [check_normal, check_7_pairs]
    def apply(method):
        return method(cards)

    return any(map(apply, win_conditions))

# Test code
if __name__ == "__main__":
    all_cards = gen_cards()
    print(len(all_cards))

    # benchmark
    start_ms = time.time()
    for i in range(1000):
        hand = random.choices(all_cards, k=14)
        check_win(hand)
    print("1000 checks took {:.2f} sec".format(time.time() - start_ms))

    # check 7 pairs
    hand = []
    for i in range(7):
        hand.append(Card(Card.NUMBER_CARD, "TONG", i+1))
        hand.append(Card(Card.NUMBER_CARD, "TONG", i+1))
    print("hand: {!s}".format(hand))
    print("check_win(hand): {}".format(check_win(hand)))

    hand = []
    hand.append(Card(Card.WIND_CARD, "ZHONG"))
    hand.append(Card(Card.WIND_CARD, "ZHONG"))
    for i in range(4):
        hand.append(Card(Card.NUMBER_CARD, "TIAO", i+1))
        hand.append(Card(Card.NUMBER_CARD, "TIAO", i+2))
        hand.append(Card(Card.NUMBER_CARD, "TIAO", i+3))
    print("hand: {!s}".format(hand))
    print("check_win(hand): {}".format(check_win(hand)))

    hand.pop()
    hand.append(Card(Card.NUMBER_CARD, "TONG", 1))
    print("hand: {!s}".format(hand))
    print("check_win(hand): {}".format(check_win(hand)))
