import pygame
from textbox import TextBox
from gamestate import GameState

class Player:


    def __init__(self, interface) -> None:
        self.interface = interface
        self.screen = interface.screen

        self.id = GameState.turn + 1

        self.name = False
        self.score = 0
        self.choice = 0

        self.name_text_box = None
        GameState.turn += 1


    def __str__(self):
        return f"Player {(self.id)}: {self.name} \nScore: {self.score}"
    


    def get_name(self):
        """
        In this function we initialise a text box so that we can get the user input from the player
        
        The players name is set within an event handler in the textbox class
        """
        textbox = TextBox(self.interface, 0, 0, 400, 50)
        textbox.center_box()
        #self.interface.text_boxes.append(textbox)
        return textbox
        
      

                