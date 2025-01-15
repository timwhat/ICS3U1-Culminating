
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
                print('Load Game')
                if player.name in gamesData:
                    if yesOrNo('Do you want to load the game? (y/n): '):
                        currentGame = gamesData[player.name]
                        result = currentGame.runGameLoop() # Game Loop
                        if not result[1]:
                            player.scoreUpdater(currentGame.size, result[0])
                        # else then it just exits out
                else: # If the player has no games
                    print('No game found for this player')
                    input('\nPress Enter to Continue')

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

