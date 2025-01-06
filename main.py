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

    # Main Loop
    # Like MAIN Main loop
    # Contains logic on selecting the player, then goes into the game loop when the player is selected
    # Works such that when they exit it loops back to user select
    while(True):
        #asks for the users name (not case sentisive)
        #loop for finding the player (either making a new player of loading an existing one)
        player = loadplayer()
        # print(player)
        # Main Menu
        choice = -1 # This just makes sure it goes into the loop, choice will get overwritten to not be -1
        while choice != 5:
            textSeperator()
            print('1. New Game')
                # Board Size
            print('2. Load Existing Game')
            print('3. Current Player Statistics')
            print('4. Leaderboard') 
            # print('5. ')  TODO Later if we have the time for the extra complexity to change the player
            print('5. Save and Exit')
        
            choice = int(input('Choose an option: '))

            # IMPORTANT: instead of having seperate new game and load functions, have one load game function
            # then when you run a new game you can just load a preset new game loadout

            if choice == 1:
                textSeperator()
                print("pretend like it ran the game (increases gameswon by 1)")
                player.gamesWon += 1
                tmpBoardSize = int(input('What would you like the board size to be?'))
                
                # TODO: Continue Board Logic

                #  to Generate board: (2d list)
                    # determine how many ducks there will be
                    # 
                # while Game Loop
                    # Print board
                    # Ask for a place on the board to shoot
                    # Check if the player has won

                #       stored as board[x][y] << indexes
                #       inside there is whether it is a duck itself, and how many ducks are in the 3x3
                #      [[True,3],[False,0]],[[True,6],[False,0]]
                #          ^ for example, this is at the coordinates (0,0), is a duck, and has 3 in the 3x3

                 
            # elif choice == 2:
            #     # TODO  Load Game
                
            elif choice == 3:
                textSeperator()
                print('Player Statistics')
                print('Name:', player.name)
                print('Games Won:', player.gamesWon)
                print('Games Lost:', player.gamesLost)
                print('Win Streak:', player.winStreak)
            # elif choice == 4:
                # leaderboard functionality to be added
            elif choice == 5:
                savePlayerData()
                break
                
            
            # TODO: Game Loop

            


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
        #self.WinRate = 1 #((gamesWon / (gamesWon + gamesLost)) * 100).toFixed(2)
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.winStreak = winStreak

    # TODO: Save player data

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

def savePlayerData():
    with open(playersDataFile,"w") as file:
        for i in playersData:
            file.write(i.name + "," + str(i.gamesWon) + "," + str(i.gamesLost) + "," + str(i.winStreak) + "\n")
            

main()