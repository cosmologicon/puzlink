import math

substring_sets = {
	"Greek letters": "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega".split(),
	"days of the week": "sun mon tue wed thu fri sat".split(),
	"months": "jan feb mar apr may jun jul aug sep oct nov dec".split(),
}

class SubstringCounter:
	def __init__(self, words):
		ntotal = sum(map(len, words))
		joined = " ".join(words)
		self.averages = {}
		for set_name, substring_set in substring_sets.items():
			n = sum(joined.count(substring) for substring in substring_set)
			self.averages[set_name] = n / ntotal

	def link(self, words):
		ntotal = sum(map(len, words))
		joined = " ".join(words)
		for set_name, substring_set in substring_sets.items():
			n = sum(joined.count(substring) for substring in substring_set)
			if n < len(words) // 2 or n < 2:
				continue
			expected = self.averages[set_name] * ntotal
			# Poisson cdf
			p = 1 - sum(math.exp(-expected) * expected ** x / math.factorial(x) for x in range(n))
			yield p * len(substring_sets), "Preponderance of %s (%s, %s, ...)" % (set_name, substring_set[0], substring_set[1])

