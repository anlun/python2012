__author__ = 'nk-karpov'

class Turn:
	def __init__(self, verdict, value):
		self._verdict = verdict
		self._value = value
	def verdict(self):
		return self._verdict
	def value(self):
		return self._value