# -*- coding: utf-8 -*-

from Card import Card

__author__ = 'anlun'

class PlayerInfo():
	# TODO: поле блок на вью карт

	def __init__(self, name, hand_cards = [], many = 0, blind = 0, ante = 0, is_hand_hidden = False):
		self.__name       = name
		self.__hand_cards = hand_cards
		self.__many       = many
		self.__blind      = blind
		self.__ante       = ante
		self.__is_hand_hidden = is_hand_hidden

		self.__is_alive = True

		# crl - change receive list
		self.__crl_cards = []
		self.__crl_many  = []
		self.__crl_blind = []
		self.__crl_ante  = []

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
	def is_hand_hidden(self):
		return self.__is_hand_hidden

	def is_alive(self):
		return self.__is_alive
	def set_is_alive(self, is_alive):
		self.__is_alive = is_alive
		# TODO: менять GUI

	# __name is unchangable
	def set_hand_cards(self, hand_cards):
		self.__hand_cards = hand_cards
		for cr in self.__crl_cards:
			cr.hand_cards_changed()

	def set_many(self, many):
		self.__many = many
		for cr in self.__crl_cards:
			cr.many_changed()
	
	def set_blind(self, blind):
		self.__blind = blind
		for cr in self.__crl_cards:
			cr.blind_changed()

	def set_ante(self, ante):
		self.__ante = ante
		for cr in self.__crl_cards:
			cr.ante_changed()

	def set_is_hand_hidden(self, is_hand_hidden):
		self.__is_hand_hidden = is_hand_hidden
		for cr in self.__crl_cards:
			cr.hand_cards_changed()	

	def add_crl_cards(self, crl_member):
		self.__crl_cards.append(crl_member)
	def add_crl_many(self, crl_member):
		self.__crl_many.append(crl_member)
	def add_crl_blind(self, crl_member):
		self.__crl_blind.append(crl_member)
	def add_crl_ante(self, crl_member):
		self.__crl_ante.append(crl_member)