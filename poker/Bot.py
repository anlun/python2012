__author__ = 'nk-karpov'

from Player import *
from Utils import *
from PlayerInfo import *
from PyQt4.QtCore import *
#from TableInfo import *


class Bot(Player):
	__player_info = None
	table_info = None
	big_blind = 0
	small_blind = 0
	bet = 0
	def __init__(self, player_info, table_info):
		self.__player_info = player_info
		self.table_info = table_info
		Player.__init__(self, player_info, table_info)
		init()

	def player_info(self):
		return self.__player_info
#	def count_raise(self):
#		log_turn = table_info.turns()
#		result = 0
# 		for turn in table:
#			if turn.verdict == 'raise':
#				result += 1
#		return result
	def btc(self, hand_mask, enemy_mask, open_mask):
		num_rem_cards = 5 - bit_count(open_mask)
		if num_rem_cards == 0:
			tmp = cmp_hand(get_list_cards_from_mask(hand_mask | open_mask),
						get_list_cards_from_mask(enemy_mask | open_mask))
			if tmp == -1:
				return 1.
			else:
				return 0.
		total_mask = open_mask | enemy_mask | open_mask
		result = 0.
		for i in xrange(len(suits) * len(values)):
			if (total_mask >> i) & 1 == 1:
				continue
			result += self.btc(hand_mask, enemy_mask, open_mask | (1 << i))
		result /= bit_count(total_mask)
		return result

	def turn_preflop(self, value):
#		count_raise = self.count_raise()
		count_raise = 0
#		position = self.table_info.get_position(self.store.name())
		position  = 1
		mask = get_mask_of_cards(self.__player_info.hand_cards())
		aa = bit_count(mask & value_masks['a']) == 2
		kk = bit_count(mask & value_masks['k']) == 2
		qq = bit_count(mask & value_masks['q']) == 2
		ak = bit_count(mask & (value_masks['a'] | value_masks['k'])) == 2
		jj = bit_count(mask & value_masks['j']) == 2
		tt = bit_count(mask & value_masks['10']) == 2
		for _value in values:
			print value_masks[_value],
		print
		for _value in values:
			print _value, value_masks[_value], mask, value_masks[_value] & mask
		print aa, kk, qq, ak, jj, tt
		print "value =", value, ", ante =", self.__player_info.ante()
		if aa | kk:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4 + value)
			elif count_raise == 1:
				return self.__raise__(self.table_info.big_blind * 4 + value)
			else:
				return self.__allin__(self.__player_info.many())
		if qq:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4 + value)
			elif count_raise == 1:
				return self.__raise__(self.table_info.big_blind * 4 + value)
			else:
				return self.__check_or_call__(value)
		if ak:
			if count_raise == 0:
				return self.__raise__(self.table_info.big_blind * 4 + value)
			elif count_raise ==  1:
				return self.__check_or_call__(value)
			else:
				if self.__player_info.ante() < value:
					return self.__fold__()
				else:
					return self.__check_or_call__(value)
		if jj | tt:
			if count_raise == 0:
				if 2 <= position and position <= 5:
					return self.__check_or_call__(value)
				else:
					return self.__raise__(self.table_info.big_blind * 4 + value)
			else:
				if self.__player_info.ante() < value:
					return self.__fold__()
				else:
					return self.__check_or_call__(value)

		for value in values:
			if bit_count(mask & value_masks[value]):
				if count_raise == 0:
					self.__check_or_call__(value)
				else:
					if self.__player_info.ante() < value:
						return self.__fold__()
					else:
						return self.__check_or_call__(value)
		if bit_count(mask & value_masks['a']) == 1 and bit_count(mask & value_masks['q']) == 1:
			if count_raise == 0:
				if position <= 5:
					return self.__fold__()
				else:
					return self.__raise__(4 * self.table_info.big_blind * 4 + value)
			else:
				if self.__player_info.ante() < value:
					return self.__fold__()
				else:
					return self.__check_or_call__(value)

		if bit_count(mask & value_masks['a']) == 1 and bit_count(mask & value_masks['j']):
			if count_raise == 0:
				if position <= 5:
					if self.__player_info.ante() < value:
						return self.__fold__()
					else:
						return self.__check_or_call__(value)
				else:
					return self.__raise__(4 * self.table_info.big_blind * 4 + value)
			else:
				if self.__player_info.ante() < value:
					return self.__fold__()
				else:
					return self.__check_or_call__(value)

		if bit_count(mask & value_masks['k']) == 1 and bit_count(mask & value_masks['q']) == 1:
			if count_raise == 0:
				if position <= 5:
					if self.__player_info.ante() < value:
						return self.__fold__()
					else:
						return self.__check_or_call__(value)
				else:
					return self.__raise__(4 * self.table_info.big_blind * 4 + value)
			else:
				if self.__player_info.ante() < value:
					return self.__fold__()
				else:
					return self.__check_or_call__(value)
		if self.__player_info.ante() < value:
			return self.__fold__()
		else:
			return self.__check_or_call__(value)

	def turn_flop(self, value):
		total = len(suits) * len(values)
		mult = 2. / (total - 5) / (total - 6)
		hand_mask = get_mask_of_cards(self.__player_info.hand_cards())
		opened_mask = get_mask_of_cards(self.table_info.opened_cards())
		probablity = 0.
		for i in xrange(52):
			if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
				continue
			for j in xrange(i):
				if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
					continue
				enemy_mask = (1 << i) | (1 << j)
				probablity += self.btc(hand_mask, enemy_mask, opened_mask)
		probablity *= mult
		if probablity > 0.75:
			return self.__raise__(self.table_info.big_blind() * 4 + value)
		elif probablity > 0.25:
			return self.__check_or_call__(value)
		else:
			if value > self.__player_info.ante():
				return self.__fold__()
			else:
				return self.__check_or_call__(value)

	def turn_turn(self, value):
		total = len(suits) * len(values)
		mult = 2. / (total - 6) / (total - 7)
		hand_mask = get_mask_of_cards(self.__player_info.hand_cards())
		opened_mask = get_mask_of_cards(self.table_info.opened_cards())
		probability = 0.
		for i in xrange(52):
			if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
				continue
			for j in xrange(i):
				if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
					continue
				enemy_mask = (1 << i) | (1 << j)
				probability += self.btc(hand_mask, enemy_mask, opened_mask)
		probability *= mult
		if probability > 0.75:
			self.bet = self.table_info.big_blind() * 4 + value
			return self.__raise__(self.table_info.big_blind() * 4 + value)
		elif probability > 0.25:
			return self.__check_or_call__(value)
		else:
			if value > self.bet:
				return self.__fold__()
			else:
				self.bet = value
				return self.__check_or_call__(value)

	def turn_river(self, value):
		total = len(suits) * len(values)
		mult = 2. / (total - 7) / (total - 8)
		hand_mask = get_mask_of_cards(self.__player_info.hand_cards())
		opened_mask = get_mask_of_cards(self.table_info.opened_cards())
		probability = 0.
		for i in xrange(52):
			if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
				continue
			for j in xrange(i):
				if hand_mask & (1 << i) != 0 or opened_mask & (1 << i) != 0:
					continue
				enemy_mask = (1 << i) | (1 << j)
				probability += self.btc(hand_mask, enemy_mask, opened_mask)
		probability *= mult
		if probability > 0.75:
			return self.__raise__(self.table_info.big_blind() * 4 + value)
		elif probability > 0.25:
			return self.__check_or_call__(value)
		else:
			if value > self.__player_info.ante():
				return self.__fold__()
			else:
				return self.__check_or_call__(value)

	def turn(self, value, blind, func_to_call):
		number_cards_on_table = len(self.table_info.opened_cards())
		print "number = ", number_cards_on_table
		for card in self.__player_info.hand_cards():
			card.__print__()
		print "ante =", self.__player_info.ante(), ", value =", value
		if number_cards_on_table == 0:
			self.bet = 0
			turn_res = self.turn_preflop(value)
		elif number_cards_on_table == 3:
			turn_res = self.turn_flop(value)
		elif number_cards_on_table == 4:
			turn_res = self.turn_turn(value)
		elif number_cards_on_table == 5:
			turn_res = self.turn_river(value)
		turn_res.verdict()
		QTimer.singleShot(1000, lambda : func_to_call(turn_res))

#	def add_message(self, message):
#		self.store.add_message(message)
