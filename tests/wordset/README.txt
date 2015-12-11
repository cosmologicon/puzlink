# Word set benchmarks

Benchmark various solutions to determine the fastest way to check for words in a word list.

Given a length-100,000 word list serialized somehow to disk, and 100 words you need to check for
inclusion in the list, what's the best serialization method?

## Main results

100 executions with `timeit`:

	run_pickle        3.72
	run_flatfile      4.45
	run_grep          8.05
	run_json_array   17.82
	run_json_object   6.43
	run_db          124.46

## Serialized file sizes

	1.2M Dec 10 22:32 wordset-array.json
	1.6M Dec 10 22:32 wordset.db
	1.8M Dec 10 22:32 wordset-object.json
	1.8M Dec 10 22:32 wordset.pkl
	911K Dec 10 22:32 wordset.txt

## Scaling results

Sqlite (db) was removed from consideration for these tests.

The word list size was adjusted between 10,000 and 1,000,000. For the most part, all methods scale
roughly linear (or slightly worse than linear) with word list size. However, json_object seems to do
well at smaller word list sizes, edging out flatfile.

The test list size was adjusted between 10 and 1,000. Here there's a significant scaling difference.
pickle, flatfile, and json_object don't scale much with test list size, but grep and json_array
scale roughly linearly. grep is the fastest method when the test list size is less than 50, but it
performs terribly when you get to larger test lists.

## Conclusion

Pickling a `set` object is the best solution, for test list sizes that we expect to see. However,
reading from a flat file into a set and using a JSONed object are both pretty good too, and the
difference is close enough that it may vary in other situations.
