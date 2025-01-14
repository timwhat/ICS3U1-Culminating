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
saveGameFile = 'save/save.json'
playersDataFile = 'save/playerData.txt'

# Regex for the username
usernameRegex = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-")

# Legend for the board
letterLegend = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# Board sizes
boardSize = [5,11]

# Board difficulties hard coded as we want everyone to play on a equal playing field
mostRevealed = .75
maxGuesses = .25

# Used to visually seperate text in the terminal
def textSeperator():
    print('\n')
    print('/************************************************************************/')
    print('\n')

# player to keep track of whos board it is
class Game: 
    def __init__(self, size, board, moves, player, numducks):
        self.size = size
        self.board = board
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

        # Handles the numbers around the ducks
        for x in range(self.size):
            for y in range(self.size):
                tempduckcount = 0
                surroundings = self.giveSurroundings(x,y)
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
                tmpGame = Game(game_data['size'], game_data['board'], game_data['moves'], player, game_data['numducks'])
                gamesData[player] = tmpGame

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

    def giveSurroundings(self,startx,starty): # returns a 2d array of a 3x3 around the given coordinates
        mainList = [[],[],[]]
        for y in range(-1,2):
            for x in range(-1,2):
                mainList[y+1].append(self.getduck(startx+x,starty+y))
        return(mainList)

    def getduck(self,x,y): # just gets the duck status of the grid tile at the position (x,y), if it is outside the board it returns False
        if (0 <= x <= self.size-1) and (0 <= y <= self.size-1):
            return self.board[x][y][0]
        return False    

    def runGameLoop(self):
        win = False
        while not win:
            # print(game.board[1],"adfadfsfasdfadsasgasdf") # Debugging
            print(self.generateBoardVisuals())
            print("what action do you want to do?")
            print("\t1. reveal a position")
            print("\t2. try to guess the amounty to guess the amount")
            print("\t3. exit (game progress will be saved)")
            decision =  inputChecker('\t\t', int)

            # Decision Tree
            if decision == 1:
                print("where do you want to check? (ex. b2, h6, etc.)")
                move = str(input())
                validmove = self.reveal(move)
                if not validmove:
                    print("invalid input")
                    input("press enter to continue:")      
                else:
                    self.moves +=1
                    if self.size**2 * maxGuesses - self.moves< 5:
                        print('You have', self.size**2 * maxGuesses - self.moves, 'moves left')
                if self.moves >= self.size**2 * maxGuesses:
                    print("You have run out of moves")
                    break
            elif decision == 2:
                print("what is your guess?")
                guess = inputChecker('', int)
                win = self.guess(guess)
                
            elif decision == 3:
                self.saveGame()
                break
        if win:
            return True
        else:
            return False
class DuckPlayer:
    def __init__(self, name, gamesWon, gamesLost, score):
        self.name = name
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.score = score
        # self.gamePoints = gamePoints

    def loadplayer(): # checks what player the user wants to log in as and then returns player 
        global playersData
        playerloaded = False
        while not playerloaded:
            name = inputChecker("Enter a username: ", str).lower()
            if not all((c in usernameRegex) for c in name):
                print("Invalid Name")
                continue
            # print("name:",name)
            alreadyexists = False
            for i in playersData:
                savedPlayer = i
                if i.name == name:
                    alreadyexists = True
                    break
            if alreadyexists:
                decision = (inputChecker("There is already a player with the name: " + name + ", Would you like to continue as this person? (y/n)", str)).lower()
                if decision == 'y':
                    player = savedPlayer
                    playerloaded = True
                elif decision == "n":
                    continue
            elif not alreadyexists:
                decision = (str(inputChecker("want to make a new profile as " + name + "? (y/n)", str))).lower()
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
                file.write(i.name + "," + str(i.gamesWon) + "," + str(i.gamesLost) + "," + str(i.score) + "\n")
    
    def scoreUpdater(self,size):
        if size == 5:
            self.score += 100
        if size == 6:
            self.score += 300
        if size == 7:
            self.score += 500
        if size == 8:
            self.score += 1000
        if size == 9:
            self.score += 2000
        if size == 10:
            self.score += 5000
        


def inputChecker(inputText, typeOfInput):
    while True:
        try:
            userInput = typeOfInput(input(inputText))
            return userInput
        except ValueError:
            continue