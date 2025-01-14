
# Imports
import random

# Import the functions and variables from the other file
from utils import *

def main():
    global playersData
    global gamesData

    # Load Saved Files
    DuckPlayer.loadPlayersData()

    # Main Game Loop
    # Contains logic on selecting the player, then goes into the game loop when the player is selected
    # Works such that when they exit it loops back to user select
    while(True):
        # Asks for the users name (not case sentisive)
        # Loop for finding the player (either making a new player of loading an existing one)
        player = DuckPlayer.loadplayer() # Player log in
        Game.loadGamesData() # Loads all of the saved games from save.json into gamesData

        # print("loaded as",gamesData)
        # s = input("size: ")
        # b = input("board: ")
        # m = input("moves: ")
        # n = input("name: ")
        # d = input("ducks: ")
        # tempgame = Game(s,b,m,n,d)
        # tempgame.saveGame()
        # print(gamesData)

        
        # Main Menu
        choice = -1 # This just makes sure it goes into the loop, choice will get overwritten to not be -1
        while choice != 5:
            textSeperator()
            print('1. New Game')
            print('2. Load Existing Game')
            print('3. Current Player Statistics')
            print('4. Leaderboard') 
            print('5. Save and Exit')
        
            choice = inputChecker('Choose an option: ', int)

            # IMPORTANT: instead of having seperate new game and load functions, have one load game function
            # then when you run a new game you can just load a preset new game loadout
            if choice == 1:
                textSeperator()
                
                # Asks for the board size
                for h,i in enumerate(range(boardSize[0],boardSize[1])):
                    print(str(h+1)+": "+str(i)+"x"+str(i))
                tmpBoardSize = inputChecker('What difficulty do you want to play?: \t', int)

                # Initializes the game object (with 0 as a temporary placeholder for ducknum)
                currentGame = Game(tmpBoardSize+4,[],0,player.name,0)
                
                # Decides how many ducks there should be, minimum a quarter of the board, maximum half
                numoftiles = (currentGame.size)**2
                currentGame.numducks = int(numoftiles //4 + (random.randint(0,100)* 0.01 * numoftiles)//4)
                # print("ducks generated:",game.numducks) # Debugging

                # Generates the board
                currentGame.generateBoard()

                print(currentGame.board)
                win = currentGame.runGameLoop() # Game Loop
                if win:
                    player.scoreUpdater(currentGame.size)
                     
            elif choice == 2:
                textSeperator()
                print('Load Game')
                if player.name in gamesData:
                    currentGame = gamesData[player.name]
                    win = currentGame.runGameLoop()
                else:
                    print('No game found for this player')
                    input('\nPress Enter to Continue')
                    continue
                if win:
                    player.scoreUpdater(currentGame.size)
                

            # Current Selected Player Statistics
            elif choice == 3:
                textSeperator()
                print('Player Statistics\n')
                print('Name:', player.name)
                print('Games Won:', player.gamesWon)
                print('Games Lost:', player.gamesLost)
                print('Score:', player.score)

                input('\nPress Enter to Continue')

            # Leaderboard
            elif choice == 4:
                # TODO Add colors to the leaderboard
                leaderboard = sorted(playersData, key=lambda x: x.score, reverse=True)
                textSeperator()
                print('Leaderboard:\n')
                for i in leaderboard:
                    print('\t' + i.name + ": " + str(i.score))
                input('\nPress Enter to Continue')
            
            # Save and Exit
            elif choice == 5:
                DuckPlayer.writePlayersData()
                Game.writeGamesData()
                return # exits out of main and stops the code
            
# Run the main function
main()

