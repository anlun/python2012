# -*- coding: utf-8 -*-

__author__ = 'anlun'

from Card import *
from PlayerInfo import *

class TableInfo:
	def __init__(self):
		# TODO: init current player // PlayerInfo
		# TODO: init enemy players (self.__enemy_list) // PlayerInfo

		# TODO: Добавить обработку обновления открытых карт для TableGui
		self.__client_player = []
		self.__enemy_list = []

		playerInfo = PlayerInfo('Vasya', [Card('h', 'a'), Card('c', '9')], 1000, 1, 200)

		self.__players = []
		self.__players.append(playerInfo)
		self.__players.append(PlayerInfo('1', [Card('h', 'a'), Card('c', '9')], 1000, 2, 200, True))
		self.__players.append(PlayerInfo('2', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('3', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('4', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('5', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('6', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('7', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))
		self.__players.append(PlayerInfo('8', [Card('h', 'a'), Card('c', '9')], 1000, 0, 200, True))

		self.__player_order_dict = {}

	def players(self):
		return self.__players

	def player_count(self):
		return len (self.__players)

	def client_player(self):
		return self.__client_player

	def enemy_players(self):
		return self.__enemy_list

	def enemy_player_count(self):
		return len (self.__enemy_list)

	# Можно сделать частью отдельного класса
	def small_blind(self):
		pass

	def big_blind(self):
		pass

	def opened_cards(self):
		# return [Card('h', 'a'), Card('c', '9'), Card('s', 'j')]
		return [Card('h', 'a'), Card('c', '9'), Card('s', 'j'), Card('d', 'k'), Card('h', 'q')]

	def bank(self):
		return 10100123213

	def player_order(self, player_name):
		if player_name in self.__player_order_dict:
			return self.__player_order_dict[player_name]
		return -1

	def __exec_msg(self):
		pass

# class TableInfo:
# 	def __init__(self, name):
# 		self.__small_blind = 0
# 		self.__big_blind = 0
# 		self.__many = 0
# 		self.__ante = 0
# 		self.__name = name

# 		# 0 - no blind
# 		# 1 - small blind
# 		# 2 - big blind
# 		self.__cur_blind = 2

# 	def new_round(self):
# 		self.__hand_cards = []
# 		self.__opened_cards = []

# 	def set_hand_cards(self, first, second):
# 		self.__hand_cards = [first, second]

# 	def add_opened_cards(self, cards):
# 		self.__opened_cards.append(cards)

# 	def hand_cards(self):
# 		""" Returns current hand cards. """
# 		return self.__hand_cards

# 	def set_blinds(self, small_blind_value, big_blind_value):
# 		self.__small_blind = small_blind_value
# 		self.__big_blind = big_blind_value

# 	def big_blind(self):
# 		return self.__big_blind

# 	def small_blind(self):
# 		return self.__small_blind

# 	def set_ante(self, ante_value):
# 		self.__ante = ante_value
	
# 	def ante(self):
# 		return self.__ante

# 	def cur_blind(self):
# 		return self.__cur_blind

# 	def opened_cards(self):
# 		""" Returns the list of already opened cards. """
# 		return self.__opened_cards

# 	def name(self):
# 		return self.__name

# 	def change_many(self, value):
# 		self.__many += value

# 	def many(self):
# 		return self.__many

# 	def add_message(self, message):
# 		pass #TODO protocol and logica
