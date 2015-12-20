# It's pretty much impossible to come up with a prior distribution of word lengths.
# So for determining whether word lengths are significant, let's just use a heuristic.

def link(lengths):
	n = len(lengths) - 1
	pfactor = 4
	if len(set(lengths)) == 1:
		yield pfactor * 0.2 ** n, "Word lengths are the same."
	else:
		if len(set(l % 2 for l in lengths)) == 1:
			parity = ("odd" if lengths[0] % 2 else "even")
			yield pfactor * 0.5 ** n, "Word lengths are all %s." % parity
		if len(set(l % 3 for l in lengths)) == 1:
			yield pfactor * 0.333 ** n, "Word lengths are equal modulo 3."
	if len(set(lengths)) == len(lengths):
		if min(lengths) + n == max(lengths):
			yield pfactor * 0.7 ** n ** 2, "Word lengths form a range of consecutive values."
		else:
			yield pfactor * 0.8 ** n ** 2, "Word lengths are all different."

