from abc import ABC, abstractmethod
from enum import Enum

class UndoError(Exception):
    pass

class InvalidTurnError(Exception):
    pass

class Turn(ABC):
    def __init__(self, player):
        self.player = player
        self.prev_player = -1

    @abstractmethod
    def apply(self, game):
        self.prev_player = game.cur_player

    @abstractmethod
    def undo(self, game):
        game.cur_player = self.prev_player

    # @abstractmethod
    # def tojson(self):
    #     pass
    #
    # @abstractmethod
    # def fromjson(self):
    #     pass

class NormalTurn(Turn):
    def __init__(self, player, drawn_card, discard):
        super().__init__(player)
        self.drawn_card = drawn_card
        self.discard = discard

    def apply(self, game):
        super().apply(game)
        p = game.players[self.player]

        if game.cards[-1] != self.drawn_card:
            raise InvalidTurnError("Normal apply: drawn card {} not consistent with deck {}".format(self.drawn_card, game.cards[-1]))
        p.cards.append(game.cards.pop())

        if self.discard not in p.cards:
            raise InvalidTurnError("Normal apply: discard {} not in hand".format(self.discard))
        p.cards.remove(self.discard)
        game.discards.append(self.discard)
        game.cur_player = (self.player + 1) % 4


    def undo(self, game):
        super().undo(game)
        p = game.players[self.player]

        if game.discards[-1] != self.discard:
            raise InvalidTurnError("Normal undo: discard {} not at top of discard pile".format(self.discard))

        p.append(game.discards.pop())

        if game.cards[-1] != self.drawn_card:
            raise UndoError("Normal undo: drawn card {} not consistent with deck {}".format(self.drawn_card, game.cards[-1]))
        p.cards.remove(self.drawn_card)
        game.cards.append(self.drawn_card)
