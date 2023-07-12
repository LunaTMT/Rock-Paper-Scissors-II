import pygame
from textbox import TextBox
from gamestate import GameState
import assets.colours as colours


class Player:


    def __init__(self, interface) -> None:
        self.interface              = interface
        self.screen                 = interface.screen

        self.sub_heading_font       = interface.sub_heading_font
        self.text_colour            = interface.text_colour
        
        self.get_centered_coord     = interface.get_centered_coord
        self.get_title_size         = interface.get_title_size

        self.id = GameState.turn + 1

        self.name = ""
        self.score = 0
        self.choice = ""

        self.name_text_box = None

        self.choice_x = 0
        self.choice_y = 1

        GameState.turn += 1


    def __str__(self):
        return f"Player {(self.id)}: {self.name}                    Score: {self.score}                     Choice: {self.choice}"
    
        
    def __repr__(self) -> str:
        return f"P{(self.id)}"
    
    def get_choice_obj(self):
        match self.choice:
            case "Rock":
                return self.interface.rock
            case "Paper":
                return self.interface.paper
            case "Scissors":
                return self.interface.scissors

        
    def draw_info(self):
        player_info = self.sub_heading_font.render(self.__str__(), True, self.text_colour)
        width, height = self.get_title_size(player_info)
        self.screen.blit(player_info,  self.get_centered_coord(width, height,  1, 0.3))

    


    def draw_choice(self):
        if self.choice:

        
            # Load the image
            choice = self.get_choice_obj()
            
            if self.name == "Computer" and self.id == 2:
                self.screen.blit(choice.image, (self.interface.choice_img_center_x, self.interface.choice_img_center_y))
            else:
                choice.move_to_center()
                self.screen.blit(choice.image, (choice.x, choice.y))


            
            




            
            

            