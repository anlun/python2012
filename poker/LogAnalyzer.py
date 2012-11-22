# -*- coding: utf-8 -*-

__author__ = "anlun"
from Card import *

class LogAnalyzer:
	def __init__(self):
		pass

	def hand_cards(self):
		""" Returns current hand cards. """
		return (Card(2, 10), Card(1, 2))

	def opened_cards(self):
		""" Returns the list of already opened cards. """
		return []
