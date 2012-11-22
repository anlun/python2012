class Card:
	def __init__(self, suit, value):
		self.__suit = suit
		self.__value = value
	
	def suit(self):
		return self.__suit
	def value(self):
		return self.__value

	def image_path(self):
		result = "images/cards/h/"
		result += str(self.__value)
		return result
