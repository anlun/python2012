# -*- coding: utf-8 -*-

__author__ = "anlun"
from Card import *

class LogAnalyzer:
	def __init__(self, name):
		self.__small_blind = 0
		self.__big_blind = 0
		self.__many = 0
		self.__ante = 0
		self.__name = name

	def new_round(self):
		self.__hand_cards = []
		self.__opened_cards = []

	def set_hand_cards(self, first, second):
		self.__hand_cards = [first, second]

	def add_opened_cards(self, cards):
		self.__opened_cards.append(cards)

	def hand_cards(self):
		""" Returns current hand cards. """
		return self.__hand_cards

	def set_blinds(self, small_blind_value, big_blind_value):
		self.__small_blind = small_blind_value
		self.__big_blind = big_blind_value

	def big_blind(self):
		return self.__big_blind

	def small_blind(self):
		return self.__small_blind

	def set_ante(self, ante_value):
		self.__ante = ante_value

	def opened_cards(self):
		""" Returns the list of already opened cards. """
		return self.__opened_cards

	def name(self):
		return self.__name

	def change_many(self, value):
		self.__many += value

	def many(self):
		return self.__many

	def add_message(self, message):
		pass #TODO protocol and logica
