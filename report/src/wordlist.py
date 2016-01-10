from collections import Counter
from src import trie

class WordList:
	def __init__(self, words):
		self.wordset = set(words)
		lengths = list(map(len, words))
		self.minwordlength = min(lengths)
		self.maxwordlength = max(lengths)
		self.lengthcounts = { n: lengths.count(n) for n in range(self.minwordlength, self.maxwordlength + 1) }

		self.anagrams = { "".join(sorted(word)): word for word in words }

		self.trie = trie.Trie(self.wordset)
		self.reverse_trie = trie.Trie(set(word[::-1] for word in self.wordset))

	def iscommonword(self, word):
		return word in self.wordset

	def iscommonanagram(self, word):
		return "".join(sorted(word)) in self.anagrams

	def getanagram(self, word):
		return self.anagrams["".join(sorted(word))]

	def nwordsbylettercount(self, length):
		return self.lengthcounts.get(length, 0)

	def common_suffixes(self, words):
		nodes = list(filter(None, [self.trie.getnode(word) for word in words]))
		for suffix, count in self.trie.common_suffixes(nodes, len(words) - 1):
			if suffix:
				yield suffix, count

	def common_prefixes(self, words):
		nodes = list(filter(None, [self.reverse_trie.getnode(word[::-1]) for word in words]))
		for suffix, count in self.reverse_trie.common_suffixes(nodes, len(words) - 1):
			if suffix:
				yield suffix[::-1], count

	def can_prepend_letter(self, word):
		return self.reverse_trie.can_extend_by_one(word[::-1])

if __name__ == "__main__":
	wordlist = WordList([line.strip() for line in open("/usr/share/dict/words")])
	for word, count in wordlist.common_prefixes_array(["gammon", "draft", "slash", "bone"]):
		print(word, count)

