from Utils import *
from TableInfo import *
from Player import *
from time import sleep
from TableGui import *

import random

class Table(QObject):
	def __init__(self, table_info):
		self.__table_info = table_info

		self.__players = [Player(player_info, self.__table_info) for player_info in self.__table_info.players()]
		self.__player_queue = self.__players

		turn_start_player_num = random.randint(0, self.__table_info.player_count() - 1)
		self.__turn_start_player_name = self.__players[turn_start_player_num].player_info().name()

		# Prepare player queue
		tsp_num = self.__player_num_by_name(self.__turn_start_player_name)	
		self.__player_queue = self.__player_queue[tsp_num : ] + self.__player_queue[ : tsp_num]

	def __player_num_by_name(self, name):
		i = 0
		for player in self.__players:
			if player.player_info().name() == name:
				return i
			i += 1

		return -1

	def __round_init(self):
		round_blind = self.__round_blind()
		self.__table_info.set_opened_cards([])

		if self.__turn_start_player_name == '':
			raise NotImplementedError()

		# Deal cards
		self.__deck = random_shuffle(generate_deck())
		for player in self.__player_queue:
			player.player_info().set_is_hand_hidden(True)
			player.player_info().set_hand_cards(self.__deck[0 : 2])
			self.__deck = self.__deck[2 : ]

		# Set blinds
		pl_inf_1  = self.__player_queue[0].player_info()
		pl_inf_1.set_blind(1)
		pl_inf_1.set_ante(round_blind / 2)
		pl_inf_1.set_many(pl_inf_1.many() - round_blind / 2)

		pl_inf_2  = self.__player_queue[1].player_info()
		pl_inf_2.set_blind(2)
		pl_inf_2.set_ante(round_blind)
		pl_inf_2.set_many(pl_inf_2.many() - round_blind)

		self.__table_info.set_bank(round_blind * 1.5)

	def __clear_round(self):
		# Open cards
		for player in self.__player_queue:
			if player.player_info().is_folded():
				continue
			player.player_info().set_is_hand_hidden(False)

		# Bank for winner
		# TODO!!!!!!

		# Clear Bank
		self.__table_info.set_bank(0)

		# Clear blinds
		for player in self.__player_queue:
			player.player_info().set_blind(0)

		# Delete dead players
		alive_players  = []
		for player in self.__player_queue:
			if player.player_info().many() > 0:
				alive_players.append(player)
				player.player_info().set_is_folded(False)
			else:
				player.player_info().set_is_alive(False)
		self.__player_queue = alive_players

		# End check
		if len(self.__player_queue) < 2:
			raise NotImplementedError()

		# Determine next tsp
		if self.__player_queue[0].player_info().name() == self.__turn_start_player_name:
			self.__player_queue = self.__player_queue[1 : ] + [ self.__player_queue[0] ]
		self.__turn_start_player_name = self.__player_queue[0].player_info().name()

	# round
	# 	init
	# 	flop
	# 	turn
	# 	river
	# 	clear

	def round(self):
		self.__round_init()
		self.__flop(self.__round_blind())

	def __flop(self, blind):
		# player for whom make_turn must be done
		self.__br_visit_list = self.__player_queue[2 : ] + self.__player_queue[0 : 2]
		self.__bets_and_raises(blind, 'flop')

	def __bets_and_raises(self, cur_ante, type):
		if self.__br_visit_list == []:
			if type == 'flop':
				self.__br_visit_list = self.__player_queue[2 : ] + self.__player_queue[0 : 2]
			else:
				self.__br_visit_list = self.__player_queue

			self.__br_visit_list = filter(lambda x: not x.player_info().is_folded(), self.__br_visit_list)

			if self.__player_queue[0].player_info().ante() == cur_ante:
				# go to next type
				if type == 'flop':
					self.__open_flop()
					return
				elif type == 'turn':
					self.__open_turn()
					return
				else:
					self.__open_river()
					return

		player = self.__br_visit_list[0]
		self.__br_visit_list = self.__br_visit_list[1 :]

		if not player.player_info().is_folded():
			# make_turn
			self.__make_player_turn(player, cur_ante, type)
		else:
			self.__bets_and_raises(cur_ante, type)

	def __clear_ante(self):
		for player in self.__player_queue:
			player.player_info().set_ante(0)

	def __make_player_turn(self, player, cur_ante, type):
		player.player_info().set_active()
		turn_res = player.turn(cur_ante)

		QTimer.singleShot(1000, lambda : self.__player_turn_res(player, turn_res, cur_ante, type))

	def __player_turn_res(self, player, turn_res, cur_ante, type):
		verdict = turn_res.verdict()

		if verdict == 'fold':
			player.player_info().set_is_folded(True)

			player.player_info().set_unactive()

			QTimer.singleShot(200, lambda : self.__bets_and_raises(cur_ante, type))
			return
		else:
			value = turn_res.value()
			many  = player.player_info().many()
			ante  = player.player_info().ante()

			player.player_info().set_many(many - value + ante)
			player.player_info().set_ante(value)

			self.__table_info.set_bank(self.__table_info.bank() + value - ante)
			player.player_info().set_unactive()

			QTimer.singleShot(200, lambda : self.__bets_and_raises(value, type))
			return

	def __open_flop(self):
		self.__table_info.set_opened_cards(self.__deck[0 : 3])
		self.__deck = self.__deck[3 : ]

		# self.__clear_ante()

		QTimer.singleShot(200, self.__turn)
	
	def __turn(self):
		self.__br_visit_list = self.__player_queue
		self.__bets_and_raises(0, 'turn')

	def __open_turn(self):
		self.__table_info.add_opened_card(self.__deck[0]) 
		self.__deck = self.__deck[1 : ]
		
		# self.__clear_ante()

		QTimer.singleShot(200, self.__river)

	def __river(self):
		self.__br_visit_list = self.__player_queue
		self.__bets_and_raises(0, 'river')

	def __open_river(self):
		self.__table_info.add_opened_card(self.__deck[0]) 
		self.__deck = self.__deck[1 : ]
		
		QTimer.singleShot(200, self.__clear_round)

	# def __bets_and_raises_flop(self, blind):
	# 	cur_ante = blind
	# 	player_ante_dict = {}
	# 	player_ante_dict[ self.__player_queue[0] ] = blind / 2
	# 	player_ante_dict[ self.__player_queue[1] ] = blind

	# 	for player in self.__player_queue[2 : ]:
	# 		# if player.player_info().is_folded():
	# 		# 	continue
	# 		cur_ante = self.__make_player_turn(player, cur_ante)
	# 		player_ante_dict[player] = cur_ante

	# 	QTimer.singleShot(200, self.__open_flop)

	# def __bets_and_raises(self, player_ante_dict, cur_ante, type):
	# 	# type is 'river' or 'turn'
	# 	while True:
	# 		old_ante = cur_ante

	# 		for player in self.__player_queue:
	# 			if player.player_info().is_folded():
	# 				continue
	# 			if player in player_ante_dict and cur_ante == player_ante_dict[player]:
	# 				return cur_ante
				
	# 			cur_ante = self.__make_player_turn(player, cur_ante)
	# 			player_ante_dict[player] = cur_ante

	# 		if old_ante == cur_ante:
	# 			return cur_ante

	def __round_blind(self):
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

if __name__ == '__main__':
	table = Table(TableInfo())