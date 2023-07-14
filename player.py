import pygame
from textbox import TextBox
from gamestate import GameState
import assets.colours as colours


class Player:


    def __init__(self, interface) -> None:
        #interface attributes
        self.interface              = interface
        self.screen                 = interface.screen
        self.scoreboard_font        = interface.scoreboard_font
        self.text_colour            = interface.text_colour
        
        #interface funcitons
        self.get_centered_coord     = interface.get_centered_coord
        self.draw_title             = interface.draw_title

        self.id = GameState.turn + 1

        self.name = ""
        self.score = 0
        self.choice = ""

        self.name_text_box = None

        self.choice_x = 0
        self.choice_y = 1

        self.score_x = 0.5
        self.score_y = 1

        GameState.turn += 1


    def __str__(self):
        return f" {(self.id)}: {self.name} Score: {self.score} Choice: {self.choice}"
    
        
    def __repr__(self) -> str:
        return f"Player {(self.id)}: {self.name} Score: {self.score} Choice: {self.choice}"
    
    def get_choice_obj(self):
        """This function return the pygame.image instance stored in the interface"""
        match self.choice:
            case "Rock":
                return self.interface.rock
            case "Paper":
                return self.interface.paper
            case "Scissors":
                return self.interface.scissors

        
    def draw_score(self):
        """
        Simply draws the players name and their score"""
        self.draw_title(self.scoreboard_font, self.name, self.score_x, self.score_y)
        self.draw_title(self.scoreboard_font, str(self.score), self.score_x, self.score_y + 0.2 )

    def draw_choice(self):
        """
        Simply draws the player's coice based upon their name
        """
        if self.choice:
        
            # Load the image
            choice = self.get_choice_obj()
            
            if self.name == "Computer" and self.id == 2:
                self.screen.blit(choice.image, (self.interface.choice_img_center_x, self.interface.choice_img_center_y))
            else:
                choice.move_to_center()
                self.screen.blit(choice.image, (choice.x, choice.y))


            
            




            
            

            