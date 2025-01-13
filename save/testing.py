import json

with open("save/testing.json","r") as file:
    f = json.load(file)

print(f["list"])

# dict1 = {
# "string" : "abcdefg",
# "list" : [1,2,3,4,5]
# }

# with open("save/testing.json","w") as file:
#     json.dump(dict1, file)