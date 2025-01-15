# This file Containes all of the functions and classes that are used in the main.py file so t can be reused, and readable

# Imports
import random
import json
import time
import os
fileDirectory = os.path.dirname(os.path.abspath(__file__))
parentDirectory = os.path.dirname(fileDirectory)

# Import to make the printed table pretty
from prettytable import PrettyTable

# Global Variables
playersData = []
gamesData = {}

# Config
saveGameFile = parentDirectory+"/save/save.json"
playersDataFile = parentDirectory+"/save/playerData.txt"

# Regex for the username
usernameRegex = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-")

# Legend for the board
letterLegend = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

# Board sizes
boardSize = [3,11]

# Board difficulties hard coded as we want everyone to play on a equal playing field
mostRevealed = .6
maxGuesses = .2

# Used to visually seperate text in the terminal
def textSeperator():
    # print('\n')
    slowPrint(0.005, '/************************************************************************/')
    print('\n')

# player to keep track of whos board it is
class Game: 
    def __init__(self, size, board, moves, player, numducks, guesses=0):
        self.size = size
        self.board = board
        self.moves = moves
        self.player = player
        self.numducks = numducks
        self.guesses = guesses

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
        try:
            y = int(pos[1])-1
            x = letterLegend.index(pos[0])

            # print(x,y,"was revealed") # Debugging

            if self.board[x][y][2] == False and (x < self.size) and (x < self.size):
                self.board[x][y][2] = True
                return True
            else:
                return False
        except (ValueError, IndexError):
            return False
    
    # 
    def guess(self,guess):
        if guess == self.numducks:
            time.sleep(1)
            textSeperator()
            print("\n\tCorrect!")
            print('*celebration noises*')
            input("press enter to continue:")
            return True
        else:
            print("\n*extremely loud incorrect buzzer noise*")
            return False

    def saveGame(self): # takes the current game after the user exits and loads it into gamesData
        global gamesData
        # print(self.player) # Debugging
        gamesData[self.player] = self
        

    def loadGamesData(): # loads the saved games data from save.json into gamesData (dictionary)
        global gamesData
        with open(saveGameFile, "r") as file:
            tmpGameData = json.load(file)
        # print("tmpgamedata is",tmpGameData)
        for player in tmpGameData:
                game_data = tmpGameData[player]
                tmpGame = Game(game_data['size'], game_data['board'], game_data['moves'], player, game_data['numducks'], game_data['guesses'])
                gamesData[player] = tmpGame

    def writeGamesData(): # writes all of the game info back into save.json
        tmpGameSave = {}
        for player in gamesData:
            game = gamesData[player]
            tmpData = {
                    'size': game.size,
                    'board': game.board,
                    'moves': game.moves,
                    'numducks': game.numducks,   
                    'guesses': game.guesses,
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
        exitGame = False
        while not win:
            movesLeft = int(self.size**2 * mostRevealed - self.moves)
            guessesLeft = int(self.size**2 * maxGuesses - self.guesses)
            # print(game.board[1],"adfadfsfasdfadsasgasdf") # Debugging
            slowPrint(0.001, self.generateBoardVisuals())
            slowPrint(0.005, "\nWhat action do you want to do?\n")
            slowPrint(0.005, "\t1. Reveal a position\n")
            slowPrint(0.005, "\t2. Try to guess the amount\n")
            slowPrint(0.005, "\t3. Exit (game progress will be saved)\n")
            slowPrint(0.005, "You have ", movesLeft, "moves and", guessesLeft, "guesses left\n")

            decision =  inputChecker('\t\t', int)

            # Decision Tree
            # Revealing a position
            if decision == 1:
                # if movesLeft < 5:
                #     print('You have', int(movesLeft), 'moves left')
                move = inputChecker('Where do you want to check? (ex. b2, h6, etc.): \t')
                validmove = self.reveal(move)
                if not validmove:
                    print("\tInvalid input")
                    input("Press enter to continue:")      
                else:
                    if movesLeft <= 1:
                        print("You ran out of moves, you can only guess now!")
                        input("\tPress enter to continue:")
                    self.moves +=1

            # Guessing the amount of ducks
            elif decision == 2:
                # if guessesLeft < 5:
                #     print('You have', int(guessesLeft + 1), 'guesses left')
                guess = inputChecker('What is your guess?\t', int)
                self.guesses += 1
                win = self.guess(guess)
                if not win and guessesLeft <= 1:
                        print('Game Over! You ran out of guesses')
                        input("\tPress enter to continue:")
                        win = False
                        break
                input("press enter to continue:")
            # Exiting the game
            elif decision == 3:
                self.saveGame()
                exitGame = True
                break
            textSeperator()
        return [win, exitGame]
    
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
                decision = yesOrNo("\nThere is already a player with the name: " + name + ", Would you like to continue as this person? (y/n):\t")
                print()
                if decision:
                    player = savedPlayer
                    playerloaded = True
                elif decision == False:
                    continue
            elif not alreadyexists:
                decision = yesOrNo("want to make a new profile as " + name + "? (y/n):\t")
                if decision:
                    player = DuckPlayer(name,0,0,0)
                    playersData.append(player)
                    playerloaded = True
                elif decision == False:
                    continue
            time.sleep(1.5)
        return player

    # Loads the player data from playerData.txt into playersData (the global list)
    def loadPlayersData():
        global playersData
        with open(playersDataFile, "r") as file:
            tmpPlayersData = file.read().strip().split("\n")

        for playerData in tmpPlayersData:
            if playerData:
                data = playerData.split(",")
                playersData.append(DuckPlayer(data[0], int(data[1]), int(data[2]), int(data[3])))

    # writes the contents of playersData (the global list) back to playerData.txt
    def writePlayersData():
        with open(playersDataFile,"w") as file:
            for i in playersData:
                file.write(i.name + "," + str(i.gamesWon) + "," + str(i.gamesLost) + "," + str(i.score) + "\n")
    
    # Updates the score of the player
    def scoreUpdater(self,size,win):
        if win:
            self.gamesWon += 1
            if size == 3:
                self.score += 30
            elif size == 4:
                self.score += 50
            elif size == 5:
                self.score += 100
            elif size == 6:
                self.score += 300
            elif size == 7:
                self.score += 500
            elif size == 8:
                self.score += 1000
            elif size == 9:
                self.score += 3000
            elif size == 10:
                self.score += 5000
        elif not win:
            self.gamesLost += 1

# Input Checker, to make sure the input is the right type
def inputChecker(inputText = '', typeOfInput = str):
    while True:
        try:
            userInput = typeOfInput(input(inputText))
            return userInput
        except ValueError:
            continue

# Yes or No input checker, so we can ask the user a yes or no question and have it abstracted
def yesOrNo(inputText):
    while True:
        userInput = input(inputText).lower()
        if userInput == "y":
            return True
        elif userInput == "n":
            return False
        else:
            continue

# slow typing
def slowPrint( delay, *args):
    text = ' '.join(map(str, args))
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    # print()
    