# -*- coding: utf-8 -*-

__author__ = 'anlun'

class Card:
	def __init__(self, suit, value):
		self.__suit = suit
		self.__value = value
	def __print__(self):
		print "(", self.__suit, ",", self.__value, ")"
	def suit(self):
		return self.__suit

	def value(self):
		return self.__value

	def image_path(self):
		return "images/cards/%s/%s.jpg" % (self.__suit, self.__value)

	def jacket_image_path(self):
		return "images/cards/d.jpg"
