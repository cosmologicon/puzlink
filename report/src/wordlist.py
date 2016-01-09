from collections import Counter

class WordList:
	def __init__(self, words):
		self.wordset = set(words)
		lengths = list(map(len, words))
		self.minwordlength = min(lengths)
		self.maxwordlength = max(lengths)
		self.lengthcounts = { n: lengths.count(n) for n in range(self.minwordlength, self.maxwordlength + 1) }

		self.anagrams = { "".join(sorted(word)): word for word in words }

		self.trie = maketrie(self.wordset)
		self.reverse_trie = maketrie(set(word[::-1] for word in self.wordset))

	def iscommonword(self, word):
		return word in self.wordset

	def iscommonanagram(self, word):
		return "".join(sorted(word)) in self.anagrams

	def getanagram(self, word):
		return self.anagrams["".join(sorted(word))]

	def nwordsbylettercount(self, length):
		return self.lengthcounts.get(length, 0)

	def common_suffixes(self, words):
		nodes = list(filter(None, [get_trie_node(self.trie, word) for word in words]))
		for suffix, count in common_suffixes(nodes, len(words) - 1):
			if suffix:
				yield suffix, count

	def common_prefixes(self, words):
		words = [word[::-1] for word in words]
		nodes = list(filter(None, [get_trie_node(self.reverse_trie, word) for word in words]))
		for suffix, count in common_suffixes(nodes, len(words) - 1):
			if suffix:
				yield suffix[::-1], count

	def can_prepend_letter(self, word):
		node = get_trie_node(self.reverse_trie, word[::-1])
		if node is None:
			return False
		return any(letter is not None and None in subnode for letter, subnode in node.items())

def maketrie(wordset):
	from collections import defaultdict
	ret = {}
	subsets = defaultdict(set)
	for word in wordset:
		if word:
			subsets[word[0]].add(word[1:])
		else:
			ret[None] = True
	for letter, subset in subsets.items():
		ret[letter] = maketrie(subset)
	return ret

def get_trie_node(trie, word):
	if word == "":
		return trie
	subtrie = trie.get(word[0])
	return None if subtrie is None else get_trie_node(subtrie, word[1:])

def common_suffixes(trie_nodes, min_common):
	if len(trie_nodes) < min_common:
		return
	counts = sum((Counter(node.keys()) for node in trie_nodes), Counter())
	for letter, count in counts.items():
		if count < min_common:
			continue
		if letter is None:
			yield "", count
		else:
			subtries = [trie_node[letter] for trie_node in trie_nodes if trie_node.get(letter)]
			for suffix, subcount in common_suffixes(subtries, min_common):
				yield letter + suffix, subcount

if __name__ == "__main__":
	wordlist = WordList([line.strip() for line in open("/usr/share/dict/words")])
	for word, count in wordlist.common_prefixes(["gammon", "draft", "slash", "bone"]):
		print(word, count)

