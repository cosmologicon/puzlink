# Determine the empirical distribution of common letter counts.

# Calculate p(m, w1, w2, ... wN), the probability that N "words" of lengths w_i will have at least
# m letters in common.

import random, math

def nshared(words):
	return len(set.intersection(*map(set, words)))

def nshared_multi(words):
	letters = set.intersection(*map(set, words))
	if not letters: return 0
	return sum(min(word.count(letter) for word in words) for letter in letters)

def randomletter():
	return random.choice("abcdefghijklmnopqrstuvwxyz")

def randomword(w):
	return "".join(randomletter() for _ in range(w))

def trial(m, ws, multi):
	words = [randomword(w) for w in ws]
	return (nshared_multi if multi else nshared)(words) >= m

def trials(m, ws, multi = False, n = 10000):
	return sum(trial(m, ws, multi) for _ in range(n)) / n

def formula1(m, ws):
	if m == 0:
		return 1
	p = 1
	for w in ws:
		p *= 1 - (1 - 1/26) ** w
	p *= 26
	return (1 - math.exp(-p)) * formula1(m - 1, [w - 1 for w in ws])



m = 5
w = 12
formula = formula1

for n in range(2, 10):
	ws = [w] * n
	print(n, trials(m, ws), trials(m, ws, multi = True), formula(m, ws))

