# Run the linker from the command line.

import pickle, sys, scipy.stats, string

words = sys.argv[1:]
words = ["".join(c for c in word if c not in string.punctuation).lower() for word in words]

linkerfile = "linker.pkl"

linker = pickle.load(open(linkerfile, "rb"))

links = []
for p, type, description in linker.link(words):
	z = -scipy.stats.norm.ppf(p)
	links.append((z, type, description))
links.sort(reverse = True)
for z, type, description in links:
	print("{:5.1f} | {:>12s} | {:s}".format(z, type, description))



