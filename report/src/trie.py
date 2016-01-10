# prefix trie for a word list on the 26 letters a-z
# designed for fast deserialization: backed by a Python arary

# nodes within the trie are implemented as array offsets.

import array

class Trie:
	def __init__(self, wordset):
		prefix_to_subset = get_prefix_to_subset(wordset)
		subset_to_offset = {prefix_to_subset[""]: 0}
		prefix_to_offset = {"": 0}
		offset_to_prefix = {0: ""}
		for prefix, subset in prefix_to_subset.items():
			if subset not in subset_to_offset:
				subset_to_offset[subset] = 27 * len(subset_to_offset)
			prefix_to_offset[prefix] = subset_to_offset[subset]
			offset_to_prefix[subset_to_offset[subset]] = prefix
		data = [None] * (27 * len(subset_to_offset))
		for offset, prefix in offset_to_prefix.items():
			data[offset] = 0 if prefix in wordset else -1
			for j, char in enumerate("abcdefghijklmnopqrstuvwxyz", 1):
				data[offset + j] = prefix_to_offset.get(prefix + char, -1)
		self.data = array.array("i")
		self.data.fromlist(data)

	def getnode(self, word):
		offset = 0
		for letter in word:
			offset = self.data[offset + ord(letter) - ord("a") + 1]
			if offset == -1:
				return None
		return offset

	# given a set of nodes corresponding to prefixes, find all suffixes that can be appended to at
	# least min_common of the prefixes to form a word, and the corresponding counts
	def common_suffixes(self, nodes, min_common):
		ncomplete = sum(self.data[node] == 0 for node in nodes)
		if ncomplete >= min_common:
			yield "", ncomplete
		for j in range(1, 27):
			subnodes = [self.data[node + j] for node in nodes if self.data[node + j] != -1]
			if len(subnodes) >= min_common:
				letter = chr(ord("a") + j - 1)
				for suffix, count in self.common_suffixes(subnodes, min_common):
					yield letter + suffix, count

	# whether there's some letter that can be added to the given word to make another word
	def can_extend_by_one(self, word):
		node = self.getnode(word)
		if node is None:
			return False
		for nextnode in self.data[node+1:node+27]:
			if nextnode != -1 and self.data[nextnode] != -1:
				return True
		return False

# mapping from a prefix string to a frozenset of suffixes that can be attached to the prefix to
# make a word
def get_prefix_to_subset(wordset):
	from collections import defaultdict
	letters_to_word_subset = defaultdict(set)
	for word in wordset:
		if not word:
			continue
		letters_to_word_subset[word[0]].add(word[1:])
	prefix_to_subset = {"": frozenset(wordset)}
	for letter, word_subset in letters_to_word_subset.items():
		prefix_to_subset[letter] = frozenset(word_subset)
		for prefix, subset in get_prefix_to_subset(word_subset).items():
			prefix_to_subset[letter + prefix] = subset
	return prefix_to_subset

if __name__ == "__main__":
	trie = Trie(["abc", "axy", "aby", "stby", "staby"])
	nodes = [trie.getnode(word) for word in ["a", "st"]]
	for suffix, count in trie.common_suffixes(nodes, 1):
		print(suffix, count)
	print(trie.can_extend_by_one("stb"))
	print(trie.can_extend_by_one("aby"))

