import duolingo
import pprint
import json

credentials = json.load(open("credentials.json", "r"))
lingo = duolingo.Duolingo(credentials["username"], credentials["password"])
response = lingo.get_lesson("Alphabet 2")
print(response)

