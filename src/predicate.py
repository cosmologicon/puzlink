
from collections import Counter

predicates = [
	("has a double letter", lambda word: any(word[i] == word[i+1] for i in range(len(word) - 1))),
	("has no repeated letters", lambda word: len(word) == len(set(word))),
	("has a single repeated letter", lambda word: len(word) == len(set(word)) + 1),
	("is in alphabetical order", lambda word: list(word) == sorted(word)),
	("starts and ends with the same letter", lambda word: word[0] == word[-1]),
]

class PredicateChecker:
	def __init__(self, words):
		n = len(words)
		nbylength = Counter(map(len, words))
		npass = Counter()
		npassbylength = Counter()
		for name, predicate in predicates:
			for word in words:
				if predicate(word):
					npass[name] += 1
					npassbylength[(name, len(word))] += 1
		self.fpass = { name: np / n for name, np in npass.items() }
		self.fpassbylength = {
			(name, length): np / nbylength[length]
			for (name, length), np in npassbylength.items()
		}
		
	def link(self, words):
		for name, predicate in predicates:
			if all(predicate(word) for word in words):
				p = 1
				f0 = self.fpass[name]
				for word in words:
					p *= self.fpassbylength.get((name, len(word)), f0)
				p *= len(predicates)
				yield p, "Every word " + name

