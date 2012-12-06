__author__ = 'nk-karpov'

from Card import Card

vtoi = {'2':0,
		'3':1,
		'4':2,
		'5':3,
		'6':4,
		'7':5,
		'8':6,
		'9':7,
		'10':8,
		'j':9,
		'q':10,
		'k':11,
		'a':12}
stoi = {'c':0,
		'd':1,
		'h':2,
		's':3}

suits = ('c', 'd', 'h', 's')
values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a')

def code_of_card(card):
	return vtoi[card.value()] * 4 + stoi[card.suit()]

def bit_count(n):
	result = 0
	for i in xrange(52):
		if  n & 1 == 1:
			result += 1
			n >>= 1
	return result

def get_mask_of_cards(cards):
	result = 0
	for card in cards:
		result |= 1 << bit_count(card)
	return result