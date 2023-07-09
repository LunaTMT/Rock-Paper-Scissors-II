import pygame
from textbox import TextBox
from gamestate import GameState


class Player:


    def __init__(self, interface) -> None:
        self.interface = interface
        self.screen = interface.screen

        self.id = GameState.turn + 1

        self.name = None
        self.score = 0
        self.choice = None

        self.name_text_box = None
        GameState.turn += 1


    def __str__(self):
        return f"Player {(self.id)}: {self.name} \nScore: {self.score} \nChoice: {self.choice}"
    
        
    def __repr__(self) -> str:
        return f"P{(self.id)}"
        


