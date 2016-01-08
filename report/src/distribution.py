# Class that keeps track of distributions of letters and n-grams.

from collections import Counter, defaultdict
import scipy.stats, math

class Distribution:
	def __init__(self, letters):
		self.letter_frequencies = get_letter_frequencies(letters)
		self.letter_moments = get_moments(self.letter_frequencies.values())
		# Binomial coefficient
		self.choose = [[1]]

	# chi-square of a match between the given letters and this distribution
	def letters_chi2(self, letters):
		ns = Counter(letters)
		n = len(letters)
		return sum((n * freq - ns[letter]) ** 2 / (n * freq) for letter, freq in self.letter_frequencies.items())

	# p-value for the chi2 test
	def letters_pvalue(self, letters):
		k = len(self.letter_frequencies) - 1
		z = (self.letters_chi2(letters) - k) / math.sqrt(2 * k)
		return scipy.stats.norm.sf(z)

	# Two lists of over- and under-represented letters (at 3 sigma) in the sample.
	def letters_outliers(self, letters):
		ns = Counter(letters)
		n = len(letters)
		high, low = [], []
		for letter, freq in self.letter_frequencies.items():
			expected = freq * n
			if (expected - ns[letter]) ** 2 / expected > 4:
				(high if ns[letter] > expected else low).append(letter)
		return high, low

	def growchoose(self, n):
		while len(self.choose) <= n:
			last = self.choose[-1]
			self.choose.append([x + y for x, y in zip([0] + last, last + [0])])

	# p-value that words of the given lengths will have at least nmatch letters in common
	def nmatch_pvalue(self, nmatch, wordlengths):
		if nmatch == 0:
			return 1 if all(wordlength >= 0 for wordlength in wordlengths) else 0
		p = (1/15) ** len(wordlengths) * self.nmatch_pvalue(nmatch - 1, [wordlength - 1 for wordlength in wordlengths])
		for w in wordlengths:
			p *= w
		return p


		self.growchoose(max(wordlengths))
		p = 1.0
		pj = math.sqrt(self.letter_moments[nmatch] * self.letter_moments[nmatch + 2])
		for w in wordlengths:
			p *= 1 - math.exp(-pj * self.choose[w][nmatch])
		return p / pj


		ncombos = 1.0
		for k in range(nmatch):
			for wordlength in wordlengths:
				ncombos *= wordlength - k
			ncombos /= 1 + k
		p = self.letter_moments[len(wordlengths)] ** nmatch
		return 1 - math.exp(-p * ncombos)
		
	# p-value that words of the given lengths will have nmatch letters in common in the same order
	def ordered_nmatch_pvalue(self, nmatch, wordlengths):
		ncombos = 1.0
		for k in range(nmatch):
			for wordlength in wordlengths:
				ncombos *= wordlength - k
				ncombos /= 1 + k
		p = self.letter_moments[len(wordlengths)] ** nmatch
		return 1 - math.exp(-p * ncombos)
		
	# probability that a set of letters of the given length will be equal to a given word.
	def match_given_prob(self, nletters):
		return (1/15) ** nletters

	# probability that a set of letters of the given length is an anagram of a given word.
	def match_given_anagram_prob(self, nletters):
		return (1/12) ** nletters

def get_letter_frequencies(letters):
	counts = Counter(letters)
	return { letter: count / len(letters) for letter, count in counts.items() }

def get_moments(freqs):
	return [sum(freq ** n for freq in freqs) for n in range(50)]


if __name__ == "__main__":
	import random
	abc = "abcdefghijklmnopqrstuvwxyz"
	words = [line.strip() for line in open("/usr/share/dict/words")]
	words = [word for word in words if all(letter in abc for letter in word)]
	letters = "".join(words)
	dist = Distribution("".join(words))
	for _ in range(10):
		letters1 = "".join(random.choice(letters) for _ in range(20))
		print(letters1, dist.letters_pvalue(letters1))
	for _ in range(10):
		letters1 = "".join(random.choice(words) for _ in range(20))[:20]
		print(letters1, dist.letters_pvalue(letters1))
	for _ in range(10):
		letters2 = "".join(random.choice("qwertyuiop") for _ in range(20))
		print(letters2, dist.letters_pvalue(letters2))
	
	for n in range(2, 12):
		w, a = 14, 2
		print(dist.nmatch_pvalue(a, [w] * n))
		s = 0
		for _ in range(10000):
			ws = [set([random.choice(abc) for _ in range(w)]) for x in range(n)]
			s += len(set.intersection(*ws)) >= a
		print(n, s / 10000)
#	print(dist.ordered_nmatch_pvalue(1, [14] * 3))


