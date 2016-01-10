Test whether a trie structure deserializes faster when its structure is simplified.


	christopher@earthbound:~/projects/puzlink/tests/trie$ time python3 make.py

	real	0m5.350s
	user	0m4.912s
	sys	0m0.436s
	christopher@earthbound:~/projects/puzlink/tests/trie$ time python3 unpickle.py trie.pkl

	real	0m0.494s
	user	0m0.448s
	sys	0m0.044s
	christopher@earthbound:~/projects/puzlink/tests/trie$ time python3 unpickle.py trie_list.pkl

	real	0m0.497s
	user	0m0.432s
	sys	0m0.064s
	christopher@earthbound:~/projects/puzlink/tests/trie$ time python3 unpickle.py trie_array.pkl

	real	0m0.073s
	user	0m0.036s
	sys	0m0.032s

Looks like arrays are faster than lists and nested dicts.
