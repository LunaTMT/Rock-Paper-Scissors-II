from player import Player

class Ai(Player):
    
    def __init__(self, interface) -> None:
        super().__init__(interface)
        self.name = "Computer"