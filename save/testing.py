import json

# with open("save/testing.json","r") as file:
#     f = json.load(file)

# print(f["list"])
# class Tester:
#     def __init__(self,s,l):
#         self.string = s
#         self.list = l

# # dict1 = {
# # "string" : "abcdefg",
# # "list" : [1,2,3,4,5]
# # }

# grester = Tester("abcdefg",[1,2,3,4,5])

# with open("save/testing.json","w") as file:
#     json.dump(grester, file)

# tmp = {
#     'colin':{'size': 1,'board': 1,'moves': 2,'numducks': 2},
#     'michael':{'size': 1,'board': 1,'moves': 2,'numducks': 2},
#     'justin':{'size': 1,'board': 1,'moves': 2,'numducks': 2}
# }

# tmp.update({'timmnmmm':{'size': 0,'board': 0,'moves': 0,'numducks': 0}})
# print(tmp)

# print(tmp['michael']['size'])

# A function that makes sure the input given is correct
def inputChecker(inputText, typeOfInput, min=0, max=0):
    while True:
        try:
            userInput = typeOfInput(input(inputText))
            if typeOfInput == str:
                return userInput
            if min <= userInput <= max:
                return userInput
        except ValueError:
            continue

inputChecker("Enter a number: ",int,1,10)
inputChecker("Enter a username: ",str)
