__author__ = 'nk-karpov'

from LogAnalyzer import *

class Player:

	def __init__(self, name):
		self.store = LogAnalyzer(name)

	def __check_or_call__(self):
		pass #TODO protocol

	def __fold__(self):
		pass #TODO protocol

	def __raise__(self, value):
		pass #TODO protocol
	def __allin__(self):
		pass #TODO protocol
	def turn(self):
		pass #TODO override

	def add_message(self, message):
		pass #TODO override and protocol all logica with analyzer and gui

	def wait(self):
		#TODO protocol
		#wait message
		#while message is not broadcast:
		#   add_message(message)
		#   continue wait
		#else:
		#   break wait
		pass
