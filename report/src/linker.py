# Linker

# linker.link(words) returns a sequence of Linkages for the associated words.

from src import distribution, wordlist, wordlengths, predicate, substring
from functools import reduce
from collections import namedtuple, Counter

Linkage = namedtuple("Linkage", ["p", "type", "description"])

class Linker:
	def __init__(self, words):
		letters = "".join(words)
		self.dist = distribution.Distribution("".join(words))
		self.wordlist = wordlist.WordList(words)
		self.predicate_checker = predicate.PredicateChecker(words)
		self.substring_counter = substring.SubstringCounter(words)

	def link(self, words, ordered = True):
		swords = list(set(words))
		generators = []
		major_awords = list(major_acrostics(words, ordered))
		awords = list(acrostics(words, ordered))
		if len(swords) >= 2:
			generators.append(("common letters", self.commonletters_links(swords)))
			generators.append(("predicate", self.predicate_links(swords)))
		if len(swords) >= 3:
			generators.append(("word length", self.wordlength_links(swords)))
			generators.append(("affixes", self.get_affix_links(swords)))
		if len(words) >= 3 and ordered:
			generators.append(("acrostic", self.acrostic_links(awords, ordered)))
			generators.append(("acrostic", self.secondary_acrostic_links(major_awords, ordered)))
		letters = "".join(words)
		if len(letters) >= 10:
			generators.append(("letter freq.", self.letterfreq_links(letters)))
			generators.append(("subwords", self.substring_counter.link(words)))

		for name, generator in generators:
			for p, description in generator:
				p *= len(generators)
				if p > 0.9:
					continue
				yield p, name, description

	def commonletters_links(self, words):
		cs = map(Counter, words)
		common = "".join(sorted(reduce(lambda a, b: a & b, cs).elements()))
		if common:
			p = self.dist.nmatch_pvalue(len(common), list(map(len, words)))
			yield p, "Letters in common: " + common

	def letterfreq_links(self, letters):
		p = self.dist.letters_pvalue(letters) * 100
		if p < 0.1:
			description = "Differs from English letter distribution."
			overrep, underrep = self.dist.letters_outliers(letters)
			if overrep:
				description += " common: %s." % "".join(overrep)
			if underrep:
				description += " uncommon: %s." % "".join(underrep)
			yield p, description

	def wordlength_links(self, words):
		for p, description in wordlengths.link(list(map(len, words))):
			yield p, description

	def predicate_links(self, words):
		for p, description in self.predicate_checker.link(words):
			yield p, description

	def acrostic_links(self, awords, ordered):
		ntest = len(awords) * 2
		for aset, aword in awords:
			if len(set(aword)) == 1:
				p = (1 / 15) ** (len(aword) - 1)
				yield p * ntest, "%s are identical (%s)" % (aset, aword[0])
			elif len(set(aword)) == 2:
				p = (2 / 15) ** (len(aword) - 2)
				yield p * ntest, "%s are all one of two (%s)" % (aset, "".join(sorted(set(aword))))

	def secondary_acrostic_links(self, awords, ordered):
		ntest = len(awords) * (2 if ordered else 1)
		for aset, aword in awords:
			if ordered and self.wordlist.iscommonword(aword):
				p = self.dist.match_given_prob(len(aword))
				p *= self.wordlist.nwordsbylettercount(len(aword))
				yield p * ntest, "%s (%s) is a common word" % (aset, aword)
			elif self.wordlist.iscommonanagram(aword):
				anagram = self.wordlist.getanagram(aword)
				p = self.dist.match_given_anagram_prob(len(aword))
				p *= self.wordlist.nwordsbylettercount(len(aword))
				yield p * ntest, "%s (%s) is an anagram of a common word (%s)" % (aset, aword, anagram)

	def get_affix_links(self, words):
		def beats(p1, p2):
			(a1, n1), (a2, n2) = p1, p2
			if n1 < n2 and len(a1) < len(a2):
				return False
			if n1 > n2:
				return True
			if len(a1) > len(a2):
				return True
			return a1 <= a2
		prefixes = list(self.wordlist.common_prefixes(words))
		for a, n in prefixes:
			if a in ["un"]:
				continue
			if all(beats((a, n), p) for p in prefixes):
				p = (1/50) ** len(words)
				if n < len(words):
					p *= 50 * len(words)
				description = ("All words" if n == len(words) else "All words but %d" % (len(words) - n))
				description += " can take a prefix: " + a
				yield p, description
		suffixes = list(self.wordlist.common_suffixes(words))
		for a, n in suffixes:
			if a in ["s", "ing", "ed", "ly"]:
				continue
			if all(beats((a, n), p) for p in suffixes):
				p = (1/50) ** len(words)
				if n < len(words):
					p *= 50 * len(words)
				description = ("All words" if n == len(words) else "All words but %d" % (len(words) - n))
				description += " can take a suffix: " + a
				yield p, description

def nth(n):
	return "%s%s" % (n, "th st nd rd th th th th th th".split()[n % 10])

def major_acrostics(words, ordered):
	yield "1st letters", "".join(word[0] for word in words)
	yield "last letters", "".join(word[-1] for word in words)
	if all(len(word) % 2 == 1 for word in words):
		yield "center letters", "".join(word[len(word) // 2] for word in words)
	if ordered and all(len(word) > n for n, word in enumerate(words)):
		yield "nth letters", "".join(word[n] for n, word in enumerate(words))
	
def acrostics(words, ordered):
	minlen = min(map(len, words))
	maxlen = max(map(len, words))
	for n in range(minlen):
		yield "%s letters" % nth(n+1), "".join(word[n] for word in words)
	if minlen != maxlen:
		for n in range(minlen):
			yield "%s letters from end" % nth(n+1), "".join(word[-1-n] for word in words)
	if ordered and all(len(word) > n for n, word in enumerate(words)):
		yield "nth letters", "".join(word[n] for n, word in enumerate(words))
	if all(len(word) % 2 == 1 for word in words):
		yield "center letters", "".join(word[len(word) // 2] for word in words)

