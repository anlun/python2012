__author__ = 'nk-karpov'

from Card import *
from random import *

value_to_int = {
		'2':0,
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
		'a':12
}

suit_to_int = {
		'c':0,
		'd':1,
		'h':2,
		's':3
}

int_to_suit = {
	0:'c',
	1:'d',
	2:'h',
	3:'s'
}

int_to_value = {
		 0:'2',
	     1:'3',
	     2:'4',
	     3:'5',
	     4:'6',
	     5:'7',
	     6:'8',
	     7:'9',
	     8:'10',
	     9:'j',
	     10:'q',
	     11:'k',
	     12:'a'
}

suits = ('c', 'd', 'h', 's')
values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a')

suit_masks  = {}
value_masks = {}
initializ = False
random = None

def init():
	global random, initializ
	random = Random()
	random.seed(239)
	if initializ:
		return None
	initializ = True
	for suit in suits:
		tmp = 0
		for value in values:
			tmp |= 1 << code_of_card(Card(suit, value))
		suit_masks[suit] = tmp
	for value in values:
		tmp = 0
		for suit in suits:
			tmp |= 1 << code_of_card(Card(suit, value))
		value_masks[value] = tmp


def bit_complete(mask):
	res = 0
	for i in xrange(len(values) * len(suits)):
		res |= 1<<(((mask>>i) & 1) ^ 1)
	return res

def is_straight_flush(list_of_cards, start):
	start_int = value_to_int[start]
	mask = get_mask_of_cards(list_of_cards)
	for suit in suits:
		target = 0
		for i in xrange(5):
			target |= 1 << code_of_card(Card(suit, int_to_value[(start_int + len(values) + i) % len(values)]))
		if mask & target == target:
			return True
		else:
			continue
	return False

def is_four(list_of_cards, value):
	mask = get_mask_of_cards(list_of_cards)
	target = 0
	for suit in suits:
		target |= 1 << code_of_card(Card(suit, value))
	return  mask & target == target

def is_full_house(list_of_cards, three, pair):
	mask = get_mask_of_cards(list_of_cards)
	if bit_count(value_masks[three] & mask) < 3:
		return False
	return bit_count(value_masks[pair] & mask) >= 2

def is_flush(list_of_cards, suit):
	mask = get_mask_of_cards(list_of_cards)
	return bit_count(mask & suit_masks[suit]) >= 5

def is_straight(list_of_cards, start):
	start_int = value_to_int[start]
	mask = get_mask_of_cards(list_of_cards)
	for i in xrange(5):
		target = 0
		for suit in suits:
			target |= 1 << code_of_card(Card(suit, int_to_value[(start_int + len(values) + i) % len(values)]))
		if target & mask == 0:
			return False
	return True

def is_three(list_of_cards, value):
	mask = get_mask_of_cards(list_of_cards)
	return bit_count(value_masks[value] & mask) >= 3

def is_two_pair(list_of_cards, first_value, second_value):
	mask = get_mask_of_cards(list_of_cards)
	return bit_count(value_masks[first_value] & mask) >= 2 and bit_count(value_masks[second_value] & mask) >= 2

def is_pair(list_of_cards, value):
	mask = get_mask_of_cards(list_of_cards)
	return bit_count(value_masks[value] & mask) >= 2

def cmp_high_card(first_list, second_list, limit):
	assert len(first_list) == len(second_list)
	sorted(first_list, key = lambda x: -value_to_int[x.value()])
	sorted(second_list, key= lambda x: -value_to_int[x.value()])
	for i in xrange(min(limit, len(first_list))):
		if first_list[i].value() > second_list[i].value():
			return -1
		if first_list[i].value() < second_list[i].value():
			return 1
	return 0

def cmp_hand(first_list, second_list):
	init()
	mask_of_first = get_mask_of_cards(first_list)
	mask_of_second = get_mask_of_cards(second_list)
	# straight flush
	for start in xrange(len(values) - 5, -2, -1):
		start_value = int_to_value[(len(values) + start) % len(values)]
		first  = is_straight_flush(first_list, start_value)
		second = is_straight_flush(second_list, start_value)
		if first or second:
			print 'straight flush'
		if first != second:
			if first:
				return -1
			else:
				return 1
		if first:
			return 0
	# four of kind
	for value in reversed(values):
		first = is_four(first_list, value)
		second = is_four(second_list, value)
		if first or second:
			print 'four'
		if first != second:
			if first:
				return -1
			else:
				return 1
		if first and second:
			mask_of_first &= bit_complete(value_masks[value])
			mask_of_second &= bit_complete(value_masks[value])
			return cmp_high_card(get_list_cards_from_mask(mask_of_first),
								 get_list_cards_from_mask(mask_of_second),
								 1)
	# full house
	for three in reversed(values):
		for pair in reversed(values):
			if pair == three:
				continue
			first = is_full_house(first_list, three, pair)
			second = is_full_house(second_list, three, pair)
			if first or second:
				print 'full house'
			if first != second:
				if first:
					return -1
				else:
					return 1
			if first and second:
				return 0
	# flush
	first = 0
	second = 0
	for suit in suits:
		if is_flush(first_list, suit):
			first = 1
			mask_of_first &= suit_masks[suit]
			break
	for suit in suits:
		if is_flush(second_list, suit):
			second = 1
			mask_of_second &= suit_masks[suit]
	if first or second:
		print 'flush'
	if first != second:
		if first:
			return  -1
		else:
			return 1
	if first and second:
		return cmp_high_card(get_list_cards_from_mask(mask_of_first),
							 get_list_cards_from_mask(mask_of_second),
							 5)
	# straight
	for start in xrange(len(values) - 5, -2, -1):
		start_value = int_to_value[(len(values) + start) % len(values)]
		first = is_straight(first_list, start_value)
		second = is_straight(second_list, start_value)
		if first or second:
			print 'straight'
		if first != second:
			if first:
				return -1
			else:
				return 1
		if first and second :
			return 0
	# three of a kind
	for value in reversed(values):
		first = is_three(first_list, value)
		second = is_three(second_list, value)
		if first or second:
			print 'three'
		if first != second:
			if first:
				return -1
			else:
				return 1
		if first and second:
			mask_of_first &= bit_complete(value_masks[value])
			mask_of_second &= bit_complete(value_masks[value])
			return cmp_high_card(get_list_cards_from_mask(mask_of_first),
								 get_list_cards_from_mask(mask_of_second),
								 2)
	# two pair
	for  first_pair in reversed(values):
		for second_pair in reversed(values):
			if value_to_int[first_pair] < value_to_int[second_pair]:
				continue
			first =  is_two_pair(first_list, first_pair, second_pair)
			second = is_two_pair(second_list, first_pair, second_pair)
			if first or second:
				print 'two pair'
			if first != second:
				if first:
					return -1
				else:
					return 1
			if first and second:
				mask_of_first &= bit_complete(value_masks[first_pair])
				mask_of_first &= bit_complete(value_masks[second_pair])
				mask_of_second &= bit_complete(value_masks[first_pair])
				mask_of_second &= bit_complete(value_masks[second_pair])
				return cmp_high_card(get_list_cards_from_mask(mask_of_first),
									get_list_cards_from_mask(mask_of_second),
									1)
	# one pair
	for value in reversed(values):
		first = is_pair(first_list, value)
		second = is_pair(second_list, value)
		if first or second:
			print 'pair'
		if first != second:
			if first:
				return -1
			else:
				return 1
		if first and second:
			mask_of_first &= bit_complete(value_masks[value])
			mask_of_second &= bit_complete(value_masks[value])
			return cmp_high_card(get_list_cards_from_mask(mask_of_first),
								 get_list_cards_from_mask(mask_of_second),
								 3)
	# high card
	print 'high card'
	return cmp_high_card(first_list, second_list, 5)

def code_of_card(card):
	return value_to_int[card.value()] * 4 + suit_to_int[card.suit()]

def reverse_code_of_card(code):
	return Card(int_to_suit[code & 3], int_to_value[code / 4])

def bit_count(n):
	result = 0
	for i in xrange(len(values) * len(suits)):
		if  n & 1 == 1:
			result += 1
		n >>= 1
	return result

def get_list_cards_from_mask(mask):
	result = []
	for i in xrange(len(values) * len(suits)):
		if  mask & (1 << i):
			result.append(reverse_code_of_card(i))
	return result

def get_mask_of_cards(cards):
	result = 0
	for card in cards:
		result |= 1 << code_of_card(card)
	return result

def random_shuffle(deck):
	for i in xrange(len(deck)):
		pos = randint(0, i)
		deck[i], deck[pos] = deck[pos], deck[i]
	return deck

def generate_deck():
	result = []
	for suit in suits:
		for value in values:
			result.append(Card(suit, value))
	return result

def top_of_deck(deck, limit):
	result = []
	for i in xrange(limit):
		result.append(deck[i])
	return result