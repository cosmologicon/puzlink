import cgi, cgitb, json, pickle
cgitb.enable(display = 0, logdir = "/tmp")

def finish(data):
	print("Content-type: application/json")
	print()
	print(json.dumps(data))
	exit()
def error(message, exception = None):
	finish({ "error": message, "exception": str(exception) })

form = cgi.FieldStorage()
try:
	query = form.getvalue("query")
#	query = '{"words":["a"],"ordered":true}'
	if len(query) > 10000:
		error("Query too long")
	query = json.loads(query)
	words = query["words"]
	ordered = query["ordered"]
	if len(words) < 1:
		error("Need at least one word")
except Exception as e:
	error("Missing or malformed query", exception = e)

with open("queries.txt", "a") as f:
	f.write(json.dumps(query) + "\n")

linkerfile = "linker.pkl"
response = { "links": [] }
try:
	linker = pickle.load(open(linkerfile, "rb"))
	for p, type, description in linker.link(words):
		response["links"].append({ "p": p, "type": type, "description": description })
except Exception as e:
	error("Server error: unable to evaluate linker", exception = e)

finish(response)
