__author__ = 'nk-karpov'

from Player import *

class Bot(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		# 2 3 4 5 6 7 8 9 10 j  q  k  a
		# 0 1 2 3 4 5 6 7 8  9 10 11 12
		self.four = map()
		for i in xrange(13):
			list_card = []
			for j in xrange(4):
				list_card.append(Card(j, i))
			self.four[i] = self.get_mask(list_card)


	def get_mask(self, list_cards):
		result = 0
		for card in list_cards:
			code = card.value() * 4 + card.suit()
			result |= 1 << code
		return result

	def bitcnt(self, n):
		res = 0
		for i in xrange(52):
			if  n & 1 == 1:
				res += 1
			n = n >> 1
		return res

	def turn_preflop(self):
		count_raise = 0
		position = 3
		mask = self.get_mask(self.store.hand_cards())
		aa = self.bitcnt(mask & self.four[12]) == 2
		kk = self.bitcnt(mask & self.four[11]) == 2
		qq = self.bitcnt(mask & self.four[10]) == 2
		ak = self.bitcnt(mask & (self.four[11] | self.fou[12])) == 2
		jj = self.bitcnt(mask & self.four[9]) == 2
		tt = self.bitcnt(mask & self.four[8]) == 2
		if aa | kk:
			if count_raise == 0:
				return self.__raise__(self.store.big_blind() * 4)
			elif count_raise == 1:
				return self.__raise__(self.store.big_blind() * 4)
			else:
				return self.__allin__()
		if qq:
			if count_raise == 0:
				return self.__raise__(self.store.big_blind() * 4)
			elif count_raise == 1:
				return self.__raise__(self.store.big_blind() * 4)
			else:
				return self.__check_or_call__()
		if ak:
			if count_raise == 0:
				return self.__raise__(self.store.big_blind() * 4)
			elif count_raise ==  1:
				return self.__check_or_call__()
			else:
				return self.__fold__()
		if jj | tt:
			if count_raise == 0:
				if position < 4:
					return self.__check_or_call__()
				else:
					return self.__raise__()
			else:
				return self.__fold__()
		return self.__fold__()

	def turn(self):
		number_cards_on_table = len(self.store.opened_cards())
		if number_cards_on_table == 0:
			return self.turn_preflop()
		elif number_cards_on_table == 3:
			self.__check_or_call__()
		elif number_cards_on_table == 4:
			self.__check_or_call__()
		elif number_cards_on_table == 5:
			self.__check_or_call__()
		else:
			assert False

	def add_message(self, message):
		self.store.add_message(message)