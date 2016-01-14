# puzlink

Tool to find patterns among sets of words.

## Set up

You will need python3 and scipy installed. If you want to use the web interface, your server needs
to run python3 (but it doesn't need scipy).

	cd report
	python3 make.py [wordlist]

`wordlist.txt` defaults to `"/usr/share/dict/words"`. The word list has two purposes. First, to get
priors on the probability that a word has certain properties, such as having a double letter.
Second, to check whether combinations of letters generated from input, such as the first letter of
every word, is a word. I recommend a medium-sized word list (100k or so). Too big and you'll get
false positives, as well as probably making it run slightly more slowly.

Setup will create a file `linker.pkl` in the `report` directory.

## Command line usage

From the report directory:

	python3 run.py word1 word2 word3 ...

Output is 3 columns: z-score of link, category, and description.

## Web usage

You can just copy the current directory onto your web server using rsync or whatever. You need to be
set up to run `report/index.py` with python3 through the url `report/`. Here's the lighttpd config
that I use:

	$HTTP["host"] =~ "(^|\.)puz\.link" {
		cgi.assign = ( ".py" => "/usr/bin/python3" )
	}

On the server, you should make the query log non-world-readable to prevent it being served:
	
	touch report/queries.txt
	chmod o-r report/queries.txt
