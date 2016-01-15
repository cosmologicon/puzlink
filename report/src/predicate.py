
from collections import Counter

predicates = [
	("has a double letter", lambda word, _: any(word[i] == word[i+1] for i in range(len(word) - 1))),
	("has no repeated letters", lambda word, _: len(word) == len(set(word))),
	("has a single repeated letter", lambda word, _: len(word) == len(set(word)) + 1),
	("is in alphabetical order", lambda word, _: list(word) == sorted(word)),
	("is in reverse alphabetical order", lambda word, _: list(word) == sorted(word, reverse = True)),
	("is close to alphabetical order", lambda word, _: sum(l1 <= l2 for l1, l2 in zip(word, word[1:])) >= len(word) - 2),
	("starts and ends with the same letter", lambda word, _: word[0] == word[-1]),
	("has a letter that appears at least 3 times", lambda word, _: Counter(word).most_common()[0][1] >= 3),
#	("ends in a shorter word", lambda word, wordlist: any(word[n:] in wordlist.wordset for n in range(1, len(word) - 2))),
	("makes another word by removing the first letter", lambda word, wordlist: word[1:] in wordlist.wordset),
	("can make another word by prepending a letter", lambda word, wordlist: wordlist.can_prepend_letter(word)),
	("alternates vowels and consonants", lambda word, _: all((l1 in "aeiou") != (l2 in "aeiou") for l1, l2 in zip(word, word[1:]))),
	("is a palindrome", lambda word, _: word == word[::-1]),
]

class PredicateChecker:
	def __init__(self, words, wordlist):
		n = len(words)
		nbylength = Counter(map(len, words))
		npass = Counter()
		npassbylength = Counter()
		for name, predicate in predicates:
			for word in words:
				if predicate(word, wordlist):
					npass[name] += 1
					npassbylength[(name, len(word))] += 1
		self.fpass = { name: np / n for name, np in npass.items() }
		self.fpassbylength = {
			(name, length): np / nbylength[length]
			for (name, length), np in npassbylength.items()
		}
		
	def link(self, words, wordlist):
		for name, predicate in predicates:
			npass = sum(predicate(word, wordlist) for word in words)
			if npass < 2 or npass < len(words) - 1:
				continue
			nfail = len(words) - npass
			description = "Every word " + ("but %d " % nfail if nfail else "")
			description += name
			p = 1
			f0 = self.fpass[name]
			for word in words[:npass]:
				p *= self.fpassbylength.get((name, len(word)), f0)
			for _ in range(nfail):
				p *= len(words)
			p *= len(predicates)
			if p < 0.9:
				yield p, description

