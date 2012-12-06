__author__ = 'nk-karpov'

from Player import *
from Utils import *
from PlayerInfo import *
#from TableInfo import *


class Bot(Player):
	store = None
	table_info = None
	big_blind = 0
	small_blind = 0

	def __init__(self, name, table_info):
		Player.__init__(self, name, table_info)
		self.store = PlayerInfo(name)
		self.table_info = table_info
		init()

#	def count_raise(self):
#		log_turn = table_info.turns()
#		result = 0
# 		for turn in table:
#			if turn.
	def turn_preflop(self):
		count_raise = self.count_raise()
		position = self.table_info.get_position(self.store.name())
		mask = get_mask_of_cards(self.store.hand_cards())
		aa = bit_count(mask & value_masks['a']) == 2
		kk = bit_count(mask & value_masks['k']) == 2
		qq = bit_count(mask & value_masks['q']) == 2
		ak = bit_count(mask & (value_masks['a'] | value_masks['k'])) == 2
		jj = bit_count(mask & value_masks['j']) == 2
		tt = bit_count(mask & value_masks['10']) == 2
		if aa | kk:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4)
			elif count_raise == 1:
				return self.__raise__(self.table_info.big_blind * 4)
			else:
				return self.__allin__()
		if qq:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4)
			elif count_raise == 1:
				return self.__raise__(self.table_info.big_blind * 4)
			else:
				return self.__check_or_call__()
		if ak:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4)
			elif count_raise ==  1:
				return self.__check_or_call__()
			else:
				return self.__fold__()
		if jj | tt:
			if count_raise == 0:
				if position < 4:
					return self.__check_or_call__()
				else:
					return self.__raise__(self.table_info.big_blind * 4)
			else:
				return self.__fold__()
		return self.__fold__()

	def turn_flop(self):

		return self.__check_or_call__()
	def turn(self):
		number_cards_on_table = len(self.table_info.opened_cards())
		if number_cards_on_table == 0:
			return self.turn_preflop()
		elif number_cards_on_table == 3:
			self.__check_or_call__()
		elif number_cards_on_table == 4:
			self.__check_or_call__()
		elif number_cards_on_table == 5:
			self.__check_or_call__()


#	def add_message(self, message):
#		self.store.add_message(message)