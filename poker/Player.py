__author__ = 'nk-karpov'

#from TableInfo import *
from Turn import *
from PyQt4.QtCore import *

class Player:
	def __init__(self, player_info, table_info):
		self.__player_info = player_info
		self.__table_info  = table_info

	def player_info(self):
		return self.__player_info

	def __check_or_call__(self, value):
		assert value >= self.player_info().ante()
		if value >= self.__player_info.many():
			return self.__allin__()
		return Turn('check or call', value)

	def __fold__(self):
		return Turn('fold', 0)

	def __raise__(self, value):
		if value <= self.__player_info.ante():
			return self.__check_or_call__(self.__player_info.ante())
		if value >= self.__player_info.many():
			return self.__allin__()
		return Turn('raise', value)

	def __allin__(self):
		self.player_info().set_is_allin(True)
		return Turn('allin', self.__player_info.many() + self.__player_info.ante())

	def is_people_player(self):
		return False
	
	def turn(self, value, blind, func_to_call):
		raise NotImplementedError()

class PeoplePlayer(Player):
	def __init__(self, player_info, table_info, decision_block):
		Player.__init__(self, player_info, table_info)
		self.__decision_block = decision_block

	def is_people_player(self):
		return True

	def turn(self, value, blind, func_to_call):
		# activate buttons
		print "gamer!!!"
		self.__decision_block.activate(value, blind, self, func_to_call)
		# self.__decision_block.activate(value, blind, None)