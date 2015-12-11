# Run this first to generate the fake data to use for benchmarks.
# Requires 2 arguments, number of words in word set, and number of words in test set:
# python3 make-data.py 100000 100

import random, sys, pickle, os, json, sqlite3

nwords = int(sys.argv[1])
ntests = int(sys.argv[2])

os.makedirs("../data", exist_ok = True)

words = map(str.strip, open("/usr/share/dict/words"))
words = [word for word in words if word.isalpha() and word.islower()]
letters = "".join(words)
lengths = list(map(len, words))

def randomword():
	return "".join(random.choice(letters) for _ in range(random.choice(lengths)))

wordset = set()
while len(wordset) < nwords:
	wordset.add(randomword())

tests = set()
for _ in range(2):
	tests.add(random.choice(list(wordset)))
while len(tests) < ntests:
	tests.add(randomword())

with open("../data/wordset-tests.txt", "w") as f:
	f.write("\n".join(tests))


with open("../data/wordset.pkl", "wb") as f:
	pickle.dump(wordset, f)

with open("../data/wordset.txt", "w") as f:
	f.write("\n".join(wordset))

with open("../data/wordset-array.json", "w") as f:
	json.dump(list(wordset), f)

with open("../data/wordset-object.json", "w") as f:
	json.dump({ word: True for word in wordset }, f)

dbfile = "../data/wordset.db"
if os.path.exists(dbfile): os.remove(dbfile)
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("CREATE TABLE words (words TEXT)")
c.executemany("INSERT INTO words VALUES (?)", [(word,) for word in wordset])
conn.commit()
conn.close()
