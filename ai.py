from player import Player
from gamestate import GameState

class Ai(Player):
    
    def __init__(self, interface) -> None:
        super().__init__(interface)
        self.name = "Computer"
        GameState.turn += 1