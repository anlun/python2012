# -*- coding: utf-8 -*-

__author__ = 'anlun'

class Card:
	def __init__(self, suit, value):
		self.__suit = suit
		self.__value = value
	
	def suit(self):
		return self.__suit

	def value(self):
		return self.__value

	def image_path(self):
		result = "images/cards/%s/%s" % (self.__suit, self.__value)
		return result
