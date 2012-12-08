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
		return Turn('check or call', value)

	def __fold__(self):
		return Turn('fold', 0)

	def __raise__(self, value):
		return Turn('raise', value)
	def __allin__(self, value):
		return Turn('allin', value)
	
	def turn(self, value, blind, func_to_call):
		# turn_res = self.__check_or_call__(10)

		# QTimer.singleShot(1000, lambda : func_to_call(turn_res))
		raise NotImplementedError()

#	def wait(self):
#		TODO protocol
#		wait message
#		while message is not broadcast:
#		   add_message(message)
#		   continue wait
#		else:
#		   break wait
#		pass

class PeoplePlayer(Player):
	def __init__(self, player_info, table_info, decision_block):
		Player.__init__(self, player_info, table_info)
		self.__decision_block = decision_block

	def turn(self, value, blind, self, func_to_call):
		# activate buttons
		self.__decision_block.activate(value, blind, func_to_call)
		# self.__decision_block.activate(value, blind, None)