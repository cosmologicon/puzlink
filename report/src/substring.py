import math

substring_sets = {
	"Greek letters": "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega".split(),
	"days of the week": "sun mon tue wed thu fri sat".split(),
	"months": "jan feb mar apr may jun jul aug sep oct nov dec".split(),
	"numbers": "one two three four five six seven eight nine ten eleven twelve zero".split(),
	"body parts": "leg arm hand foot knee elbow ankle neck head ear eye nose mouth hair lip tongue chin face back calf thigh".split(),
	"consecutive letters": "ab bc cd de ef fg gh hi ij jk kl lm mn no op pq qr rs st tu uv vw wx xy yz".split(),
	"consecutive letter trios": "abc bcd cde def efg fgh ghi hij ijk jkl klm lmn mno nop opq pqr qrs rst stu tuv uvw vwx wxy xyz".split(),
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

