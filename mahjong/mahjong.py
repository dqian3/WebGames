import random
from collections import deque
from enum import Enum

from cards import Card, gen_cards, check_win
from turn import NormalTurn

class Choice(Enum):
    PASS = "PASS"
    NORMAL = "NORMAL"
    CHI = "CHI"
    PENG = "PENG"
    WIN = "WIN"

class OutOfTurnError(Exception):
    pass


class Player:
    def __init__(self):
        self.cards = []
        self.points = 0

    def check_peng(self, discard):
        playable = list(filter(lambda c: not c.used, self.cards))
        return playable.count(discard) == 2

    def check_chi(self, discard):
        if (discard.card_type != Card.NUMBER_CARD): return False

        playable = list(filter(lambda c: not c.used, self.cards))
        chi_cards = [False] * 5
        prev = discard.prev_card()
        next = discard.next_card()

        if (prev in playable and next in playable): return True
        if (prev in playable and prev.prev_card() in playable): return True
        if (next in playable and next.next_card() in playable): return True

        return False

    def check_hu(self, discard):
        return check_win(self.cards + [discard])

class Mahjong:
    def __init__(self):
        self.cards = deque()
        self.players = [Player(), Player(), Player(), Player()]

        # Queue of players that can make a move
        self.choices = deque()
        self.history = deque()

        self.cur_player = 0
        self.discards = deque()

    def start(self):
        for c in gen_cards():
            self.cards.append(c)

        for i in range(13):
            for player in self.players:
                player.cards.append(self.cards.pop())

        self.gen_choices()

    def gen_choices(self):
        self.choices.clear()

        if (len(self.discards) > 0):
            discard = self.discards[-1]
            for i, player in enumerate(self.players, self.cur_player):
                if (player.check_hu(discard)):
                    self.choices.append((i % 4, Choice.HU))

            for i, player in enumerate(self.players, self.cur_player):
                if (player.check_peng(discard)):
                    self.choices.append((i % 4, Choice.PENG))

            if (self.players[self.cur_player].check_chi(discard)):
                self.choices.append((self.cur_player, Choice.CHI))

        # TODO check zimo

        self.choices.append((self.cur_player, Choice.NORMAL))

    def make_move(self, player, choice, turn=None):
        if (len(self.choices) == 0):
            raise OutOfTurnError("No choices present!")

        (player, next_choice) = self.choices[0]
        if (player != turn.player):
            raise OutOfTurnError("Wrong player!")

        # Player chooses not to take turn (ie. skips PENG)
        if (choice == Choice.PASS):
            if (next_choice == Choice.NORMAL):
                raise OutOfTurnError("Pass normal turn?")

            self.choices.pop_left()
            return

        # Apply turn (updates cards), append to history, generate new choices
        assert(turn is not None)
        turn.apply(self)
        self.history.append(turn)
        self.gen_choices()


    def undo(self):
        if len(self.history) == 0:
            raise UndoError("Nothing to undo!")

        turn = self.history.pop()
        turn.undo(self)
        self.gen_choices()


# Testing
if __name__ == "__main__":
    game = Mahjong()
    game.start()

    print ("==== Before Turn 1 ====")
    print(game.choices)
    print(game.cards[-1])
    for i, player in enumerate(game.players, 1):
        print("{} cards: {}".format(i, player.cards))

    turn1 = NormalTurn(0, game.cards[-1], game.players[0].cards[0])
    game.make_move(0, Choice.NORMAL, turn1)
    print ("==== After Turn 1 ====")
    print(game.players[0].cards)
    print(game.discards[-1])

    print ("==== Before Turn 2 ====")
    print(game.choices)
    print(game.cards[-1])
    for i, player in enumerate(game.players, 1):
        print("Player {} cards: {}".format(i, player.cards))
