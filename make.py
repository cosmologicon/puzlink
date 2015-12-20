# Create a Linker object.

from src import linker
import pickle, string

wordfile = "/usr/share/dict/words"
outfile = "linker.pkl"

words = [line.strip() for line in open(wordfile)]
words = [word for word in words if all(letter in string.ascii_lowercase for letter in word)]
obj = linker.Linker(words)

pickle.dump(obj, open(outfile, "wb"))

