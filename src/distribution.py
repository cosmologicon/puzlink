# Class that keeps track of distributions of letters and n-grams.

from collections import Counter, defaultdict
import scipy.stats, math

class Distribution:
	def __init__(self, letters):
		self.letter_frequencies = get_letter_frequencies(letters)
		self.letter_moments = get_moments(self.letter_frequencies.values())

	# chi-square of a match between the given letters and this distribution
	def chi2(self, letters):
		ns = Counter(letters)
		n = len(letters)
		return sum((n * freq - ns[letter]) ** 2 / (n * freq) for letter, freq in self.letter_frequencies.items())

	# p-value for the chi2 test
	def pvalue(self, letters):
		k = len(self.letter_frequencies) - 1
		z = (self.chi2(letters) - k) / math.sqrt(2 * k)
		return scipy.stats.norm.sf(z)

def get_letter_frequencies(letters):
	counts = Counter(letters)
	return { letter: count / len(letters) for letter, count in counts.items() }

def get_moments(freqs):
	return [sum(freq ** n for freq in freqs) for n in range(50)]


if __name__ == "__main__":
	import random
	words = [line.strip() for line in open("/usr/share/dict/words")]
	words = [word for word in words if all(letter in "abcdefghijklmnopqrstuvwxyz" for letter in word)]
	letters = "".join(words)
	dist = Distribution("".join(words))
	for _ in range(10):
		letters1 = "".join(random.choice(letters) for _ in range(20))
		print(letters1, dist.pvalue(letters1))
	for _ in range(10):
		letters1 = "".join(random.choice(words) for _ in range(20))[:20]
		print(letters1, dist.pvalue(letters1))
	for _ in range(10):
		letters2 = "".join(random.choice("qwertyuiop") for _ in range(20))
		print(letters2, dist.pvalue(letters2))

