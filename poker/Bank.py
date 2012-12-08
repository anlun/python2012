__author__ = 'nk-karpov'


class Bank:
	__set_of_player = set()
	__many = 0
	def __init__(self):
		self.__set_of_player = set()
		self.__many = 0

	def many(self):
		return self.__many

	def set_of_player(self):
		return self.__set_of_player

	def add_bet(self, name, value):
		self.__many += value
		if name not in self.__set_of_player:
			self.__set_of_player = self.__set_of_player | {name}

	def del_player(self, name):
		self.__set_of_player.remove(name)
