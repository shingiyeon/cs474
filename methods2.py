import jsonlines
import json
path = "./data/dev.jsonlines"
f = open(path, "r")

ex = [json.loads(jsonline) for jsonline in f.readlines()]
f.close()

g = open("./data/dev2.jsonlines", "w")
for i in ex[:100]:
    g.write(json.dumps(i))
    g.write("\n")
g.close()
