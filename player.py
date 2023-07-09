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

        self.name = None
        self.score = 0
        self.choice = None

        self.name_text_box = None

        GameState.turn += 1


    def __str__(self):
        return f"Player {(self.id)}: {self.name}                    Score: {self.score}                     Choice: {self.choice}"
    
        
    def __repr__(self) -> str:
        return f"P{(self.id)}"
    
    def get_choice_image(self):
        match self.choice:
            case "Rock":
                return self.interface.rock_img
            case "Paper":
                return self.interface.paper_img
            case "Scissors":
                return self.interface.scissors_img

        
    def draw_info(self):
        player_info = self.sub_heading_font.render(self.__str__(), True, self.text_colour)
        width, height = self.get_title_size(player_info)
        self.screen.blit(player_info,  self.get_centered_coord(width, height,  1, 0.3))

    def draw_choice(self):
        if self.choice:
            # Load the image
            choice_img = self.get_choice_image()
            img_width, img_height = choice_img.get_width(), choice_img.get_height()
            

            # Set the rectangle dimensions
            rect_width = 210
            rect_height = 150

            # Create a rectangle surface

            rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            rect_surface.fill((255, 215, 0, 128))  # Fill with red color

            # Calculate the position to center the image on the rectangle surface
            image_x = (rect_width - img_width) // 2
            image_y = (rect_height - img_height) // 2

            # Blit the image onto the rectangle surface at the center position
            rect_surface.blit(choice_img, (image_x, image_y))

            # Blit the rectangle surface onto the screen at a specific position

      

            self.screen.blit(rect_surface, self.get_centered_coord(rect_width, rect_height, 0, 1))