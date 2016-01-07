import cgi, cgitb, json, pickle
from lib import config, report, util
cgitb.enable(display = 0, logdir = "/tmp")

def finish(data):
	print("Content-type: application/json")
	print()
	print(json.dumps(data))
	exit()
def error(message):
	finish({ "error": message })

form = cgi.FieldStorage()
try {
	query = form.getvalue("query")
	if len(query) > 10000:
		error("Query too long")
	query = json.parse(query)
	words = query["words"]
	ordered = query["ordered"]
	if len(words) < 1:
		error("Need at least one word")
} except {
	error("Missing or malformed query")
}

# with open("queries.txt", "a") as f:
# 	f.write(json.dump(query) + "\n")

linkerfile = "linker.pkl"
response = { "links": [] }
try {
	linker = pickle.load(open(linkerfile, "rb"))
	for p, type, description in linker.link(words):
		response["links"].append({ "p": p, "type": type, "description": description })
} except {
	error("Server error: unable to evaluate linker")
}

finish(response)
