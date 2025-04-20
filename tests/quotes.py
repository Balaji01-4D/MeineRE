import json
import random
with open("./tests/test.json",'r') as file:
    lst = json.load(file)
if (lst):
    print(random.choice(lst))
else:
    print("Meine")
