import assets.colours as colours

class GameState:

    turn = 0
    current_button = None
    current_player = None
    players = None

    @staticmethod
    def get_next_player():
        GameState.turn += 1
        GameState.current_player = GameState.players[GameState.turn % 2]

        print(GameState.players[GameState.turn % 2].id)
        print(GameState.players, GameState.turn % 2, f"Current Player: {GameState.current_player.name}")
            
    @staticmethod
    def set_current_choice(choice):
        GameState.current_player.choice = choice