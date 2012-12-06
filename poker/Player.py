__author__ = 'nk-karpov'

#from TableInfo import *

class Player:

	def __init__(self, name, table_info):
		pass
	def __check_or_call__(self):
		return ["check or call", None]

	def __fold__(self):
		return ["fold", None]

	def __raise__(self, value):
		return ["raise", value]
	def __allin__(self):
		pass #TODO protocol
	def turn(self):
		pass #TODO override

	def add_message(self, message):
		pass #TODO override and protocol all logica with analyzer and gui

#	def wait(self):
#		TODO protocol
#		wait message
#		while message is not broadcast:
#		   add_message(message)
#		   continue wait
#		else:
#		   break wait
#		pass
