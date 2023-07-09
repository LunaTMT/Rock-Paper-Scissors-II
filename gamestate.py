import assets.colours as colours
import random

class GameState:

    turn = 0
    current_button = None
    current_player = None
    players = None

    @staticmethod
    def get_next_player():
        GameState.turn += 1
        GameState.current_player = GameState.players[GameState.turn % 2]

         
    @staticmethod
    def set_current_choice(choice):
        #first player set name
        GameState.current_player.choice = choice
        
        #get ai player and set random choice of words
        GameState.get_next_player()
        GameState.current_player.choice = random.choice(('Rock', 'Paper', 'Scissors'))

        #get next player, i.e. first player
        GameState.get_next_player()