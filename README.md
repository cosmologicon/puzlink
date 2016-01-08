# puzlink

Tool to find patterns among sets of words.

## Set up

	cd report
	python3 make.py [wordlist]

`wordlist.txt` defaults to `"/usr/share/dict/words"`. The word list has two purposes. First, to get
priors on the probability that a word has certain properties, such as having a double letter.
Second, to check whether combinations of letters generated from input, such as the first letter of
every word, is a word.

Setup will create a file `linker.pkl`.

## Command line usage

	python3 run.py word1 word2 word3 ...

Output is 3 columns: z-score of link, category, and description.

