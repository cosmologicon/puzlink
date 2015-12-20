# Linker

# linker.link(words) returns a sequence of Linkages for the associated words.

from src import distribution, wordlengths
from collections import namedtuple

Linkage = namedtuple("Linkage", ["p", "type", "description"])

class Linker:
	def __init__(self, words):
		letters = "".join(words)
		self.dist = distribution.Distribution("".join(words))

	def link(self, words):
		for p, description in self.wordlength_links(words):
			yield p * 2, "word length", description
		for p, description in self.letterfreq_links(words):
			yield p * 2, "letter freq.", description

	def letterfreq_links(self, words):
		letters = "".join(words)
		if len(letters) < 10:
			return
		p = self.dist.letters_pvalue(letters)
		if p < 0.1:
			yield p, "Differs from English letter distribution."		

	def wordlength_links(self, words):
		if len(words) < 3:
			return
		for p, description in wordlengths.link(list(map(len, words))):
			yield p, description


