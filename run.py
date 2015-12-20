# Run the linker from the command line.

import pickle, sys

words = sys.argv[1:]

linkerfile = "linker.pkl"

linker = pickle.load(open(linkerfile, "rb"))

for p, type, description in linker.link(words):
	print(p, type, description)

