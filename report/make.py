# Create a Linker object.

from src import linker
import pickle, string, sys

wordfile = "/usr/share/dict/words" if len(sys.argv) <= 1 else sys.argv[1]
outfile = "linker.pkl"

words = [line.strip() for line in open(wordfile, encoding="latin-1")]
words = [word for word in words if all(letter in string.ascii_lowercase for letter in word)]
obj = linker.Linker(words)

pickle.dump(obj, open(outfile, "wb"))

