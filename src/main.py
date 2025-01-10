import ast
import random
from prettytable import PrettyTable

from utils import *

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

                game.generateBoard()

                print(game.board)
                
                win = False
                while not win:
                    # print(game.board[1],"adfadfsfasdfadsasgasdf")
                    print(game.generateBoardVisuals())
                    print("what action do you want to do?")
                    print("1. reveal a position")
                    print("2. try to guess the amounty to guess the amount")
                    decision =  int(input())
                    if decision == 1:
                        print("where do you want to check? (ex. b2, h6, etc.)")
                        move = str(input())
                        validmove = game.reveal(move)
                        if not validmove:
                            print("invalid input")
                            input("press enter to continue:")       
                    elif decision == 2:
                        print("what is your guess?")
                        guess = int(input())
                        win = game.guess(guess)
                player.gamesWon += 1
                 
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

# main()

lst = ast.literal_eval("[['Here we want everything other than the board such as stats on ducks, whos playing on this board'], ['SECOND THE ACTUAL BOARD']]") 
print(lst[0])