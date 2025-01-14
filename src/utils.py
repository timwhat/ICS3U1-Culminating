# This file Containes all of the functions and classes that are used in the main.py file so t can be reused, and readable

# Imports
import random
import json

# Import to make the printed table pretty
from prettytable import PrettyTable

# Global Variables
playersData = []
gamesData = {}

# Config
saveGameFile = '../save/save.json'
playersDataFile = '../save/playerData.txt'

# Regex for the username
usernameRegex = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-")

# Legend for the board
letterLegend = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# Board sizes
boardSize = [5,11]

# Used to visually seperate text in the terminal
def textSeperator():
    print('\n')
    print('/************************************************************************/')
    print('\n')

# player to keep track of whos board it is
class Game: 
    def __init__(self, size, moves, player, numducks):
        self.size = size
        self.board = []
        self.moves = moves
        self.player = player
        self.numducks = numducks

    # Generates the game board for the first time (when starting the game)
    def generateBoard(self):
        self.board = []
        tempCoords = []

        # Initializes the board without anything
        for x in range(self.size):
            column = []
            for y in range(self.size):
                column.append([False,"a",False])
                tempCoords.append([x,y])
            self.board.append(column)

        # Randomly places the ducks on the board
        for i in range(self.numducks):
            coords = random.choice(tempCoords)
            tempCoords.remove(coords)
            # print(coords,"was determined to be a duck")
            self.board[coords[0]][coords[1]][0] = True

        # TODO Delete this at the end (was a temporary visualizer before generateBoardVisuals was made)
        # for y in range(self.size): 
        #     temprow = ""
        #     for x in range(self.size):
        #         if self.board[x][y][0]:
        #             temprow += "1"
        #         elif not self.board[x][y][0]:
        #             temprow = temprow + "0"
    
        # Handles the numbers around the ducks
        for x in range(self.size):
            for y in range(self.size):
                tempduckcount = 0
                surroundings = giveSurroundings(x,y,self)
                for row in surroundings:
                    for tile in row:
                        if tile:
                            tempduckcount += 1
                self.board[x][y][1] = tempduckcount

    # Generates the board to the terminal (uses prettytable)
    def generateBoardVisuals(self):
        # Initializing the table
        table = PrettyTable()

        # Adding the legend
        tmpLetterLegend = []
        tmpNumLegend = []
        for i in range(self.size):
            tmpLetterLegend.append(' ' +letterLegend[i] + ' ')
            tmpNumLegend.append(i+1)

        # Write the header Legend
        table.field_names = [""] + tmpLetterLegend
                
        # Adding the rows
        for i in range(self.size):
            # A tmp list to store the row as elements get added to it
            showedRow = []
            for j in range(self.size):
                # Chosing whcih items to display
                if self.board[j][i][2]:
                    if self.board[j][i][0]:
                        showedRow.append("D")
                    else:
                        showedRow.append(str(self.board[j][i][1]))
                else:
                    showedRow.append("-")
            # Write the row to the table, along with the side legend
            table.add_row([str(tmpNumLegend[i])] + showedRow, divider=True)
        return table

    # Sets the grid tile at that position's index of 2 to True
    def reveal(self, pos):
        y = int(pos[1])-1
        x = letterLegend.index(pos[0])

        # print(x,y,"was revealed") # Debugging

        if self.board[x][y][2] == False and (x < self.size) and (x < self.size):
            self.board[x][y][2] = True
            return True
        else:
            return False
    
    # 
    def guess(self,guess):
        if guess == self.numducks:
            print("correct!")
            return True
        else:
            print("*extremely loud incorrect buzzer noise*")
            input("press enter to continue:")
            return False

    def saveGame(self): # takes the current game after the user exits and loads it into gamesData
        global gamesData
        print(self.player)
        gamesData[self.player] = self
        

    def loadGamesData(): # loads the saved games data from save.json into gamesData (dictionary)
        global gamesData
        with open(saveGameFile, "r") as file:
            tmpGameData = json.load(file)
        print("tmpgamedata is",tmpGameData)
        for player in tmpGameData:
                game_data = tmpGameData[player]
                game = Game(game_data['size'], game_data['board'], game_data['moves'], game_data['numducks'])
                gamesData[player] = game

    def writeGamesData(): # writes all of the game info back into save.json
        tmpGameSave = {}
        for player in gamesData:
            game = gamesData[player]
            tmpData = {
                    'size': game.size,
                    'board': game.board,
                    'moves': game.moves,
                    'numducks': game.numducks   
                }
            tmpGameSave[player] = tmpData

        with open(saveGameFile, 'w') as file:
            json.dump(tmpGameSave, file, indent=4)   

class DuckPlayer:
    def __init__(self, name, gamesWon, gamesLost, winStreak):
        self.name = name
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.winStreak = winStreak
        # self.gamePoints = gamePoints

    def loadplayer(): # checks what player the user wants to log in as and then returns player 
        global playersData
        playerloaded = False
        while not playerloaded:
            name = input("Enter a username: ").lower()
            # print("name:",name)
            alreadyexists = False
            for i in playersData:
                savedPlayer = i
                if i.name == name:
                    alreadyexists = True
                    break
            if alreadyexists:
                decision = (inputChecker("There is already a player with the name: " + name + ", Would you like to continue as this person? (y/n)", ['y', 'n', 'Y', 'N'])).lower()
                if decision == 'y':
                    player = savedPlayer
                    playerloaded = True
                elif decision == "n":
                    continue
            elif not alreadyexists:
                decision = (str(inputChecker("want to make a new profile as " + name + "? (y/n)", ['y', 'n', 'Y', 'N']))).lower()
                if decision == 'y':
                    player = DuckPlayer(name,0,0,0)
                    playersData.append(player)
                    playerloaded = True
                elif decision == "n":
                    continue
        return player

    def loadPlayersData():
        global playersData
        with open(playersDataFile, "r") as file:
            tmpPlayersData = file.read().strip().split("\n")

        for playerData in tmpPlayersData:
            if playerData:
                data = playerData.split(",")
                playersData.append(DuckPlayer(data[0], int(data[1]), int(data[2]), int(data[3])))

    def writePlayersData(): # writes the contents of playersData (the global list) back to playerData.txt
        with open(playersDataFile,"w") as file:
            for i in playersData:
                file.write(i.name + "," + str(i.gamesWon) + "," + str(i.gamesLost) + "," + str(i.winStreak) + "\n")
                
    def giveSurroundings(startx,starty,game): # returns a 2d array of a 3x3 around the given coordinates
        mainList = [[],[],[]]
        for y in range(-1,2):
            for x in range(-1,2):
                mainList[y+1].append(getduck(startx+x,starty+y,game))
        return(mainList)

    def getduck(x,y,game): # just gets the duck status of the grid tile at the position (x,y), if it is outside the board it returns False
        if (0 <= x <= game.size-1) and (0 <= y <= game.size-1):
            return game.board[x][y][0]
        else:
            return False


# def inputChecker(inputText, typeOfInput, min=0, max=0):
#     while True:
#         try:
#             userInput = typeOfInput(input(inputText))
#             if typeOfInput == str:
                
#                 return userInput
#             if min <= userInput <= max:
#                 return userInput
#         except ValueError:
#             continue

def inputChecker(prompt, allowedInputs): # A function that makes sure the input given is correct
    while True:
        newinput = input(prompt)
        if newinput.isnumeric():
            newinput = float(newinput)
            if newinput % 1 == 0:
                newinput = int(newinput)
        if newinput in allowedInputs:
            return newinput
        else:
            print("invalid input, try again")

# number = inputChecker("pick a number between 0 and 9 and also a to c on the alphabet also is valid for some reason",[1,2,3,4,5,6,7,8,9,0,"a","b","c"])