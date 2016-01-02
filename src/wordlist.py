
class WordList:
	def __init__(self, words):
		self.wordset = set(words)
		lengths = list(map(len, words))
		self.minwordlength = min(lengths)
		self.maxwordlength = max(lengths)
		self.lengthcounts = { n: lengths.count(n) for n in range(self.minwordlength, self.maxwordlength + 1) }

	def iscommonword(self, word):
		return word in self.wordset

	def nwordsbylettercount(self, length):
		return self.lengthcounts.get(length, 0)

