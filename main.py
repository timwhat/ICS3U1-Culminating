import random

# Config
saveGameFile = 'save.txt'
playeDataFile = 'playerData.txt'

# Global Variables
playerData = {}
gameData = {}

def main():
    # Before Game Checks
    # TODO: Check if save file exists
    # TODO: Check if player data file exists if not, create it, else load it
    
    # Main Game Loop
    while(True):
        
        # TODO: Ask for player name or play under existing name

        # TODO: Main Menu
            # 1. New Game
                # 1. Board Size
            # 2. Load Game
            # 3. Player Stats
            # 4. Leaderboard
            # 5. Change Player
            # 6. Exit
        
        # TODO: Game

# TODO: Load Previous Game/player data to lists

class Game: # player to keep track of whos board it is
    def __init__(self, size, moves, player):
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.moves = moves
        self.player = player

    def printBoard(self):
        # TODO: Print the board

    def makeMove(self, x, y):
        # TODO: Make a move on the board
    
    def checkWin(self):
        # TODO: Check if the player has won
        # idk if we should intergrate as its own or in makeMove function

    def saveGame(self):
        # TODO: Save the game to a file    

class DuckPlayer:
    def __init__(self, name, WinLoss, gamesWon, gamesLost, winStreak):
        self.name = name
        self.WinLoss = WinLoss
        self.gamesWon = gamesWon
        self.gamesLost = gamesLost
        self.winStreak = winStreak

    # TOOO: Game Won / Lost

    # TODO: Save player data

main()