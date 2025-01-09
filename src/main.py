import random
from prettytable import PrettyTable

from utils import *

# Config
saveGameFile = 'save/save.txt'
playersDataFile = 'save/playerData.txt'

# Global Variables
playersData = []
gamesData = []

usernameRegex = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-")
letterLegend = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

def main():

    global playersData
    global gamesData

    # Load Saved Files
    DuckPlayer.loadSavedFiles()

    # Main Game Loop
    # Contains logic on selecting the player, then goes into the game loop when the player is selected
    # Works such that when they exit it loops back to user select
    while(True):
        #asks for the users name (not case sentisive)
        #loop for finding the player (either making a new player of loading an existing one)
        player = DuckPlayer.loadplayer()
        # Main Menu
        choice = -1 # This just makes sure it goes into the loop, choice will get overwritten to not be -1
        while choice != 5:
            textSeperator()
            print('1. New Game')
            print('2. Load Existing Game')
            print('3. Current Player Statistics')
            print('4. Leaderboard') 
            print('5. Save and Exit')
        
            choice = int(input('Choose an option: '))

            # IMPORTANT: instead of having seperate new game and load functions, have one load game function
            # then when you run a new game you can just load a preset new game loadout

            if choice == 1:
                textSeperator()

                for h,i in enumerate(range(5,11)):
                    print(str(h+1)+": "+str(i)+"x"+str(i))
                tmpBoardSize = int(input('What difficulty do you want to play?'))

                # initializes the game object (with 0 as a temporary placeholder for ducknum)
                game = Game(tmpBoardSize+4,0,player.name,0)
                
                # decides how many ducks there should be, minimum a quarter of the board, maximum half
                numoftiles = (game.size)**2
                numofducks = int(numoftiles//4 + (random.randint(0,100)* 0.01 * numoftiles)//4)
                print("ducks generated:",numofducks)
                game.numducks = numofducks

                game.generateboard()

                print(game.board)
                
                leave = False
                while not leave:
                    # print(game.board[1],"adfadfsfasdfadsasgasdf")
                    game.printBoard()
                    print("what action do you want to do?")
                    print("1. reveal a position")
                    print("2. try to guess the amounty to guess the amount")
                    decision =  int(input)
                    if decision == 1:
                        print("where do you want to check? (ex. b2, h6, etc.)")
                        move = str(input())
                        game.makeMove(move)
                    elif decision == 2:
                        print("what is your guess?")
                        guess = int(input())
                        game.guess(guess)

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
                print('Player Statistics\n')
                print('Name:', player.name)
                print('Games Won:', player.gamesWon)
                print('Games Lost:', player.gamesLost)
                print('Win Streak:', player.winStreak)

                input('\nPress Enter to Continue')
            elif choice == 4:
                # TODO Add colors to the leaderboard
                leaderboard = sorted(playersData, key=lambda x: x.gamesWon, reverse=True)
                textSeperator()
                print('Leaderboard:\n')
                for i in leaderboard:
                    print('\t' + i.name + ": " + str(i.gamesWon))
                input('\nPress Enter to Continue')
            elif choice == 5:
                DuckPlayer.savePlayerData()

def textSeperator():
    print('\n')
    print('/************************************************************************/')
    print('\n')

class Game: # player to keep track of whos board it is
    def __init__(self, size, moves, player, numducks):
        self.size = size
        self.board = []
        self.moves = moves
        self.player = player
        self.numducks = numducks

    #TODO reverse the x and y of board to print that with the add_rows
    # then add logic for what is revealed
    def printBoard(self):
        table = PrettyTable()
        tmpLegend = []
        tmpNumLegend = []
        # Adding the legend
        for i in range(self.size):
            tmpLegend.append(letterLegend[i])
            tmpNumLegend.append(i+1)
        # table.add_column([""] + tmp_legend)
                
        table.add_column("", tmpNumLegend)
        for i in range(self.size):
            # tmp.extend(self.board[i])
            table.add_column(str(i+1), self.board[i])
        print(table)

    def generateboard(self):
        self.board = []
        tempCoords = []
        for x in range(self.size):
            column = []
            for y in range(self.size):
                column.append([False,"a",False])
                tempCoords.append([x,y])
            self.board.append(column)

        for i in range(self.numducks):
            coords = random.choice(tempCoords)
            tempCoords.remove(coords)
            # print(coords,"was determined to be a duck")
            self.board[coords[0]][coords[1]][0] = True

        for y in range(self.size):
            temprow = ""
            for x in range(self.size):
                if self.board[x][y][0]:
                    temprow = temprow + "1"
                elif not self.board[x][y][0]:
                    temprow = temprow + "0"

        for x in range(self.size):
            for y in range(self.size):
                tempduckcount = 0
                surroundings = giveSurroundings(x,y,self)
                for row in surroundings:
                    for tile in row:
                        if tile:
                            tempduckcount += 1
                self.board[x][y][1] = tempduckcount

    def reveal(self, pos):
        y = int(pos[1])-1
        x = letterLegend.index(pos[0])
        print(x,y)

    
    def guess(self,guess):
        if guess == self.numducks:
            print("correct!")

    # def saveGame(self):
    #     # TODO: Save the game to a file    

class DuckPlayer:
    def __init__(self, name, gamesWon, gamesLost, winStreak):
        self.name = name
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.winStreak = winStreak

    def loadplayer():
        global playersData
        playerloaded = False
        
        while not playerloaded:
            name = str((str(input("enter name:\t"))).lower())
            # REGEX CHECK
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
                
def giveSurroundings(startx,starty,game):
    mainList = [[],[],[]]
    for y in range(-1,2):
        for x in range(-1,2):
            mainList[y+1].append(getduck(startx+x,starty+y,game))
    return(mainList)

def getduck(x,y,game):
    if (0 <= x <= game.size-1) and (0 <= y <= game.size-1):
        return game.board[x][y][0]
    else:
        return False

main()