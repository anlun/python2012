__author__ = 'nk-karpov'

class Player(object):

    def __init__(self):
        self.__many = 0
        self.__hand = 0
        self.__small_blind = 0
        self.__big_blind = 0
        self.__ante = 0
        self.__log_turn = []
        self.__name = "empty bot"

    def __check__(self):
        return ["check", None]

    def __fold__(self):
        return ["fold", None]

    def __raise__(self, value):
        if value is not int:
            RuntimeError()
        return ["raise", value]

    def turn(self, value):
        pass

    def add_many(self, value):
        self.__many += value

    def set_blinds(self, small_blinds_value):
        self.__small_blind = small_blinds_value
        self.__big_blind = 2 * small_blinds_value

    def set_ante(self, ante_value):
        self.__ante = ante_value

    def small_blind(self):
        result = min(self.__many, self.small_blind)
        self.__many -= self.__small_blind
        return result

    def big_blind(self):
        result = min(self.__many, self.__big_blind)
        self.__many -= self.__big_blind
        return result

    def ante(self):
        result = min(self.__many, self.__ante)
        self.__many -= self.__ante
        return result

    def many(self):
        return self.__many

    def set_hand(self, hand):
        self.__hand = hand

    def add_log_turn(self, log_turn):
        self.__log_turn.append(log_turn)

    def new_round(self):
        pass