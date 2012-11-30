# -*- coding: utf-8 -*-

__author__ = "anlun"

from Card import *

class AbstractPlayerInfo:
	def name(self):
		raise NotImplementedError()
	def hand_cards(self):
		raise NotImplementedError()
	def many(self):
		raise NotImplementedError()
	def blind(self):
		raise NotImplementedError()
	def ante(self):
		raise NotImplementedError()

class PlayerInfo(AbstractPlayerInfo):
	def __init__(self, name, hand_cards, many, blind = 0, ante = 0):
		self.__name       = name
		self.__hand_cards = hand_cards
		self.__many       = many
		self.__blind      = blind
		self.__ante       = ante

	def name(self):
		return self.__name
	def hand_cards(self):
		return self.__hand_cards
	def many(self):
		return self.__many
	def blind(self):
		return self.__blind
	def ante(self):
		return self.__ante

	# __name is unchangable

	def set_hand_cards(self, hand_cards):
		self.__hand_cards = hand_cards
	def set_many(self, many):
		self.__many = many
	def set_blind(self, blind):
		self.__blind = blind
	def set_ante(self, ante):
		self.__ante = ante	