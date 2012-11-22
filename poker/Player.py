__author__ = 'nk-karpov'

class Player(object):
    __many = 0
    __hand = 0
    __small_blind = 0
    __big_blind = 0
    __ante = 0
    __name = None

    def __init__(self, name):
        assert name is str
        __name = name

    def __check_or_call__(self):
        pass #TODO protocol

    def __fold__(self):
        pass #TODO protocol

    def __raise__(self, value):
        pass #TODO protocol

    def turn(self, value):
        pass #TODO override

    def add_many(self, value):
        self.__many += value

    def set_blinds(self, small_blind_value, big_blind_value):
        self.__small_blind = small_blind_value
        self.__big_blind = big_blind_value

    def set_ante(self, ante_value):
        self.__ante = ante_value

    def put_small_blind(self):
        self.__many -= min(self.__many, self.__small_blind)

    def put_big_blind(self):
        result = min(self.__many, self.__big_blind)
        self.__many -= self.__big_blind
        return result

    def put_ante(self):
        self.__many -= min(self.__many, self.__ante)

    def many(self):
        return self.__many

    def set_hand(self, hand):
        self.__hand = hand

    def add_message(self, message):
        pass #TODO override and protocol all logica with analyzer and gui

    def wait(self):
        #TODO protocol
        #wait message
        #while message is not broadcast:
        #   add_message(message)
        #   continue wait
        #else:
        #   break wait
        pass
