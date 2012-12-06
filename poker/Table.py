from Utils import *
from TableInfo import *
from Player import *

import random

class Table:
	def __init__(self):
		self.__table_info = TableInfo()
		self.__turn_start_player = random.randint(0, TableInfo.player_count() - 1)

		self.__players = [Player(player_info) for player_info in self.__table_info.players()]

	def new_round(self):
		new_round_blind = self.__new_round_blind()
		self.__table_info.set_opened_cards([])

		turn_start_player = self.__turn_start_player
		if turn_start_player == -1 or :
			raise NotImplementedError()

		# Deal cards
		self.__deck = random_shuffle(generate_deck())
		for player in self.__players:
			player.player_info().set_is_hand_hidden(True)
			player.player_info().set_hand_cards(self.__deck[0:2])
			self.__deck = self.__deck[2:]

		# Prepare player queue
		self.__player_queue = self.__table_info.players()[turn_start_player:] + self.__table_info.players()[turn_start_player:]

		# Set blinds
		self.__player_queue[0]

		# Start turns
		self.__flop()
		self.__turn()
		self.__river()

		turn_start_player = self.__next_alive_player(self.__turn_start_player)
		# Delete dead players

	def __flop(self):
		self.__bets_and_raises()
		self.__table_info.set_opened_cards(self.__deck[0:4])
		self.__deck = self.__deck[4:]
	
	def __turn(self):
		self.__bets_and_raises()
		self.__table_info.add_opened_card(self.__deck[0]) 
		self.__deck = self.__deck[0:]

	def __river(self):
		self.__turn()

	def __bets_and_raises(self):
		for player in self.__player_queue:


	def __new_round_blind(self):
		return 10

	def __next_alive_player(self, player_num):
		result = player_num + 1
		for player in self.__table_info.players()[player_num + 1:]:
			if player.is_alive():
				return result
			result += 1

		result = 0
		for player in self.__table_info.players()[0 : player_num]:
			if player.is_alive():
				return result
			result += 1

		return -1

		