from player import Player
from gamestate import GameState
import random

class Ai(Player):
    
    def __init__(self, interface) -> None:
        super().__init__(interface)
        self.id = 2  
        self.name = "Computer"

        self.choice_x = 2
        self.choice_y = 1

    def get_choice(self):
        self.choice = random.choice(('Rock', 'Paper', 'Scissors'))