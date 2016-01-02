# Linker

# linker.link(words) returns a sequence of Linkages for the associated words.

from src import distribution, wordlist, wordlengths
from collections import namedtuple

Linkage = namedtuple("Linkage", ["p", "type", "description"])

class Linker:
	def __init__(self, words):
		letters = "".join(words)
		self.dist = distribution.Distribution("".join(words))
		self.wordlist = wordlist.WordList(words)

	def link(self, words, ordered = True):
		generators = []
		awords = list(acrostics(words))
		if len(words) >= 3:
			generators.append(("word length", self.wordlength_links(words)))
		if len(words) >= 3 and ordered:
			generators.append(("acrostic", self.acrostic_links(awords)))
		letters = "".join(words)
		if len(letters) >= 10:
			generators.append(("letter freq.", self.letterfreq_links(letters)))
		
		for name, generator in generators:
			for p, description in generator:
				yield p * len(generators), name, description

	def letterfreq_links(self, letters):
		p = self.dist.letters_pvalue(letters)
		if p < 0.1:
			yield p, "Differs from English letter distribution."		

	def wordlength_links(self, words):
		for p, description in wordlengths.link(list(map(len, words))):
			yield p, description

	def acrostic_links(self, awords):
		for aset, aword in awords:
			if self.wordlist.iscommonword(aword):
				p = self.dist.match_given_prob(len(aword))
				p *= self.wordlist.nwordsbylettercount(len(aword))
				yield p * len(awords), "%s (%s) is a common word" % (aset, aword)

def nth(n):
	return "%s%s" % (n, "th st nd rd th th th th th th".split()[n % 10])

def acrostics(words):
	minlen = min(map(len, words))
	maxlen = max(map(len, words))
	for n in range(minlen):
		yield "%s letters" % nth(n+1), "".join(word[n] for word in words)
	if minlen != maxlen:
		for n in range(minlen):
			yield "%s letters from end" % nth(n+1), "".join(word[-1-n] for word in words)
	if all(len(word) > n for n, word in enumerate(words)):
		yield "nth letters", "".join(word[n] for n, word in enumerate(words))
	if all(len(word) % 2 == 1 for word in words):
		yield "center letters", "".join(word[len(word) // 2] for word in words)

