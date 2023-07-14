"""This class keeps track of the state of the game"""
class GameState:

    turn = 0
    current_button = None
    current_player = None
    players = None

    @staticmethod
    def get_next_player() -> None:
        """
        This function increments the current turn and then changes the current player based upon the turn
        Takes advantage of the parity of numbers and the continual switching between 0 and 1 for %2
        """
        GameState.turn += 1
        GameState.current_player = GameState.players[GameState.turn % 2]


         
    @staticmethod
    def set_current_choice(choice) -> None:
        """
        This function simple sets the choice of the current player 
        """
        print("setting")
        GameState.current_player.choice = choice
        GameState.get_next_player()
        