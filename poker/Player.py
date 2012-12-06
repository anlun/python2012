__author__ = 'nk-karpov'

#from TableInfo import *
from Turn import *

class Player:

	def __init__(self, name, table_info):
		pass
	def __check_or_call__(self, value):
		return Turn("check or call", value)

	def __fold__(self):
		return Turn("fold", 0)

	def __raise__(self, value):
		return Turn("raise", value)
	def __allin__(self, value):
		return Turn("allin", value)
	def turn(self, value):
		raise NotImplementedError

#	def wait(self):
#		TODO protocol
#		wait message
#		while message is not broadcast:
#		   add_message(message)
#		   continue wait
#		else:
#		   break wait
#		pass
