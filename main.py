import random

# Config
saveGameFile = 'save.txt'
playersDataFile = 'playerData.txt'

# Global Variables
playersData = []
gamesData = []

# {playerdata.name = justin, play...}
# {playerdata.name = colin, ...}

def main():

    global playersData
    global gamesData

    # Load Saved Files
    loadSavedFiles()

    # Main Game Loop
    while(True):
        #asks for the users name (not case sentisive)
        #loop for finding the player (either making a new player of loading an existing one)
        player = loadplayer()
        print(player)
        # Main Menu
        textSeperator()
        print('1. New Game')
        print('2. Load Existing Game')
        print('3. Current Player Statistics')
        print('4. Leaderboard')
        # print('5. ')
        print('5. Save and Exit')
            # 1. New Game
                # 1 Board Size
            # 2. Load Game
            # 3. Player Stats
            # 4. Leaderboard
            # 5. Change Player TODO Later if we have the time for the extra complexity
            # 6. Save and Exit
        # choice = int(input())
        # if choice == 1:
        #     textSeperator()
        #     tmpBoardSize = int(input('What would you like the board size to be?'))
            
            # TODO: Continue Board Logic
        # elif choice == 2:
        # elif choice == 3:
        # elif choice == 4:
        # elif choice == 5:
            # savePlayerData()
            
        
        # TODO: Game


def textSeperator():
    print('\n')
    print('/************************************************************************/')
    print('\n')

class Game: # player to keep track of whos board it is
    def __init__(self, size, moves, player):
        self.size = size
        self.board = [size, size]
        self.moves = moves
        self.player = player

    # def printBoard(self):
    #     # TODO: Print the board

    # def makeMove(self, x, y):
    #     # TODO: Make a move on the board
    
    # def checkWin(self):
    #     # TODO: Check if the player has won
    #     # idk if we should intergrate as its own or in makeMove function

    # def saveGame(self):
    #     # TODO: Save the game to a file    

class DuckPlayer:
    def __init__(self, name, gamesWon, gamesLost, winStreak):
        self.name = name
        self.WinLossPercentage = ((gamesWon / (gamesWon + gamesLost)) * 100).toFixed(2)
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.winStreak = winStreak

    # TODO: Save player data

def loadSavedFiles():
    global playersData
    global gamesData

    with open(playersDataFile, "r") as file:
        tmpPlayersData = file.read().strip().split("\n")
    with open(saveGameFile, "r") as file:
        gamesData = file.read().strip().split("\n")

    for playerData in tmpPlayersData:
        if playerData:
            data = playerData.split(",")
            playersData.append(DuckPlayer(data[0], int(data[1]), int(data[2]), int(data[3])))


def loadplayer():
    global playersData
    playerloaded = False
    
    while not playerloaded:
        name = str((str(input("enter name:\t"))).lower())
        # print("name:",name)
        alreadyexists = False
        for i in playersData:
            savedPlayer = i
            if i.name == name:
                alreadyexists = True
                break
        if alreadyexists:
            decision = ''
            while decision not in ["y","n"]:
                decision = (str(input(("There is already a player with the name: " + name + ", Would you like to continue as this person? (y/n)")))).lower()
            if decision == 'y':
                player = savedPlayer
                playerloaded = True
            elif decision == "n":
                continue
        elif not alreadyexists:
            decision = ''
            while decision not in ["y","n"]:
                decision = (str(input(("want to make a new profile as " + name + "? (y/n)")))).lower()
            if decision == 'y':
                player = DuckPlayer(name,0,0,0)
                playersData.append(player)
                playerloaded = True
            elif decision == "n":
                continue
    return player

def savePlayerData():
    with open(playersDataFile,"w") as file:
        for i in playersData:
            file.write(i.name + "," + i.gamesWon + "," + i.gamesLost + "," + i.winStreak + "\n")
            

main()