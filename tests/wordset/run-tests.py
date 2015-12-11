# Run timeit over the data

import random, sys, pickle, os, json, sqlite3, timeit

ntrials = int(sys.argv[1])

tests = [line.strip() for line in open("../data/wordset-tests.txt")]

def run_pickle():
	wordset = pickle.load(open("../data/wordset.pkl", "rb"))
	return sum(test in wordset for test in tests)

def run_flatfile():
	wordset = set(line.strip() for line in open("../data/wordset.txt"))
	return sum(test in wordset for test in tests)

def run_grep():
	wordfile = open("../data/wordset.txt").read()
	return sum("\n" + test + "\n" in wordfile for test in tests)

def run_json_array():
	wordset = json.load(open("../data/wordset-array.json"))
	return sum(test in wordset for test in tests)

def run_json_object():
	wordset = json.load(open("../data/wordset-object.json"))
	return sum(test in wordset for test in tests)

def run_db():
	conn = sqlite3.connect("../data/wordset.db")
	c = conn.cursor()
	ret = 0
	for test in tests:
		c.execute("SELECT words FROM words WHERE words = (?)", (test,))
		ret += c.fetchone() is not None
	conn.close()
	return ret

#for fname in ["run_pickle", "run_flatfile", "run_grep", "run_json_array", "run_json_object", "run_db"]:
for fname in ["run_pickle", "run_flatfile", "run_grep", "run_json_array", "run_json_object"]:
	print(fname, eval(fname + "()"), timeit.timeit(fname + "()", number = ntrials, setup = "from __main__ import tests, " + fname))

