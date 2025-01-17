
# Imports
import random
import time

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

    textSeperator()

    print("Welcome to Ducksweeper!")

    while(True):
        # Asks for the users name (not case sentisive)
        # Loop for finding the player (either making a new player of loading an existing one)
        player = DuckPlayer.loadplayer() # Player log in
        Game.loadGamesData() # Loads all of the saved games from save.json into gamesData
        
        # Main Menu
        choice = -1 # This just makes sure it goes into the loop, choice will get overwritten to not be -1
        while choice != 5:
            textSeperator()
            slowPrint(0.002, '1. New Game\n')
            slowPrint(0.002, '2. Load Existing Game\n')
            slowPrint(0.002, '3. Current Player Statistics\n')
            slowPrint(0.002, '4. Leaderboard\n')
            slowPrint(0.002, '5. Save and Exit\n')
            choice = inputChecker('Choose an option: ', int)
            print()
            time.sleep(0.5)

            # IMPORTANT: instead of having seperate new game and load functions, have one load game function
            # then when you run a new game you can just load a preset new game loadout
            if choice == 1:
                textSeperator()
                
                # Asks for the board size
                for h,i in enumerate(range(boardSize[0],boardSize[1])):
                    slowPrint(0.002, str(h+1)+": "+str(i)+"x"+str(i)+'\n')
                tmpBoardSize = inputChecker('\nWhat difficulty do you want to play?: \t', int)
                textSeperator()
                
                # Initializes the game object (with 0 as a temporary placeholder for ducknum)
                currentGame = Game(tmpBoardSize+boardSize[0]-1,[],0,player.name,0)
                numoftiles = (currentGame.size)**2 # determines the number of total tiles in the board
                 # Decides how many ducks there should be, minimum a quarter of the board, maximum half
                currentGame.numducks = int(numoftiles //4 + (random.randint(0,100)* 0.01 * numoftiles)//4)
                currentGame.generateBoard() # Generates the board
                result = currentGame.runGameLoop() # Game Loop

                if not result[1]:
                    player.scoreUpdater(currentGame.size, result[0])
                # else then it just exits out
            
            elif choice == 2:
                textSeperator()
                slowPrint(0.02, 'Checking Games...\n')
                if player.name in gamesData:
                    if yesOrNo('Previous game found, would you like to load that game? (y/n): '):
                        textSeperator()
                        currentGame = gamesData[player.name]
                        result = currentGame.runGameLoop() # Game Loop
                        if not result[1]:
                            player.scoreUpdater(currentGame.size, result[0])
                        # else then it just exits out
                else: # If the player has no games
                    print('No game found for this player')
                    input('\n\tPress Enter to Continue')

            # Current Selected Player Statistics
            elif choice == 3:
                textSeperator()
                print('Player Statistics\n')
                print('Name:', player.name)
                print('Games Won:', player.gamesWon)
                print('Games Lost:', player.gamesLost)
                print('Score:', player.score)

                input('\n\tPress Enter to Continue')

            # Leaderboard
            elif choice == 4:
                leaderboard = sorted(playersData, key=lambda x: x.score, reverse=True)
                textSeperator()
                slowPrint(0.005,'Leaderboard:\n\n')
                for i in leaderboard:
                    slowPrint(0.005,'\t' + i.name + ": " + str(i.score)+'\n')
                input('\n\tPress Enter to Continue')
            
            # Save and Exit
            elif choice == 5:
                DuckPlayer.writePlayersData()
                Game.writeGamesData()
                textSeperator()
                slowPrint(0.1, '\tThanks for playing!\n\n')
                time.sleep(2)
                slowPrint(0.05, '\tSaving and Exiting')
                slowPrint(0.2, '.......\n\n')
                return # exits out of main and stops the code
            
# Run the main function
main()

