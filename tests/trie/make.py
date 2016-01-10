import pickle, string, array
from collections import defaultdict

words = [line.strip() for line in open("/home/christopher/Downloads/ukacd.txt", encoding = "latin-1")]
words = [word for word in words if all(letter in string.ascii_lowercase for letter in word)]

def maketrie(wordset):
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

trie = maketrie(set(words))	

def addnode(trie_list, offset0, node):
	for j, letter in enumerate([None] + list("abcdefghijklmnopqrstuvwxyz")):
		if letter in node:
			subnode = node[letter]
			if subnode == True:
				trie_list[offset0 + j] = 0
			else:
				offset = len(trie_list)
				trie_list[offset0 + j] = offset
				trie_list += [None] * 27
				addnode(trie_list, offset, subnode)
		else:
			trie_list[offset0 + j] = -1

trie_list = [None] * 27
addnode(trie_list, 0, trie)

trie_array = array.array("i")
trie_array.fromlist(trie_list)

pickle.dump(trie, open("trie.pkl", "wb"))
pickle.dump(trie_list, open("trie_list.pkl", "wb"))
pickle.dump(trie_array, open("trie_array.pkl", "wb"))


