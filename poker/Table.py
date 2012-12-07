from Utils import *
from TableInfo import *
from Player import *

import random

class Table:
	def __init__(self):
		self.__table_info = TableInfo()

		self.__players = [Player(player_info, self.__table_info) for player_info in self.__table_info.players()]
		self.__player_queue = self.__players

		turn_start_player_num = random.randint(0, self.__table_info.player_count() - 1)
		self.__turn_start_player_name = self.__players[turn_start_player_num].player_info().name()

		# Prepare player queue
		tsp_num = self.__player_num_by_name(self.__turn_start_player_name)	
		self.__player_queue = self.__player_queue[tsp_num : ] + self.__player_queue[ : tsp_num]

		# test
		self.round()

	def __player_num_by_name(self, name):
		i = 0
		for player in self.__players:
			if player.player_info().name() == name:
				return i
			i += 1

		return -1

	def round(self):
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
		self.__player_queue[0].player_info().set_blind(1)
		self.__player_queue[0].player_info().set_ante(round_blind / 2)

		self.__player_queue[1].player_info().set_blind(2)
		self.__player_queue[1].player_info().set_ante(round_blind)

		# Start turns
		self.__flop(round_blind)
		self.__turn()
		self.__river()

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

		# Delete dead players / have no many for blind
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

	def __flop(self, blind):
		self.__bets_and_raises_flop(blind)
		self.__table_info.set_opened_cards(self.__deck[0 : 3])
		self.__deck = self.__deck[3 : ]
	
	def __turn(self):
		self.__bets_and_raises({}, 0)
		self.__table_info.add_opened_card(self.__deck[0]) 
		self.__deck = self.__deck[0 : ]

	def __river(self):
		self.__turn()

	def __bets_and_raises_flop(self, blind):
		cur_ante = blind
		player_ante_dict = {}
		player_ante_dict[ self.__player_queue[0] ] = blind / 2
		player_ante_dict[ self.__player_queue[1] ] = blind

		for player in self.__player_queue[2 : ]:
			if player.player_info().is_folded():
				continue
			cur_ante = self.__make_player_turn(player, cur_ante)
			player_ante_dict[player] = cur_ante

		self.__bets_and_raises(player_ante_dict, cur_ante)

	def __bets_and_raises(self, player_ante_dict, cur_ante):
		while true:
			old_ante = cur_ante

			for player in self.__player_queue:
				if player.player_info().is_folded():
					continue
				if player in player_ante_dict and cur_ante == player_ante_dict[player]:
					return cur_ante
				
				cur_ante = self.__make_player_turn(player, cur_ante)
				player_ante_dict[player] = cur_ante

			if old_ante == cur_ante:
				return cur_ante

	def __make_player_turn(self, player, cur_ante):
		turn_res = player.turn(cur_ante)
		verdict = turn_res.verdict()

		if verdict == 'fold':
			player.player_info().set_is_folded(True)
			return cur_ante
		else:
			value = turn_res.value()
			many  = player.player_info().many()
			ante  = player.player_info().ante()

			player.player_info().set_many(many - value + ante)
			player.player_info().set_ante(ante)

			self.__table_info.set_bank(self.__table_info.bank() + value - ante)
			return value

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
	table = Table()