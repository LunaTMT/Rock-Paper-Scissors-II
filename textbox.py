import pygame
import assets.colours as colours

from pygame.locals import *
from gamestate import GameState

class TextBox:
    id = 0

    def __init__(self, interface, x, y, width, height) -> None:
        self.interface = interface
        self.screen = interface.screen

        self.user_input = ""
        self.default_text = "Please enter your name"
        
        self.width = width 
        self.height = height
        self.x = x
        self.y = y
        
        self.rect_colour = colours.WHITE
        self.text_colour = colours.BLACK

        self.font = pygame.font.Font(None, 36)
        self.hover = False
        self.input_active = False

        self._set_rect()

    def center_box(self) -> None:
        """
        This function simple centers the box based on its proportions and calls the update method to set the rectangle again
        """
        center_x = (self.screen.get_width() - self.width) // 2 
        center_y = (self.screen.get_height() - self.height) // 2
        self.x = center_x
        self.y = center_y 
        self._set_rect()
        
        
    def _set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    
    def draw(self) -> None:
        
        """Blits the players name above textbox"""
        text = f"Player {GameState.current_player.id}"
        font = pygame.font.Font(None, 32)
        text_surface = self.font.render(text, True, colours.BLACK)
        self.screen.blit(text_surface, (self.x + 15, self.y - font.size(text)[1]  ))

        #hover to gold
        self.rect_colour = colours.GOLD if self.hover else colours.WHITE
        
        #Necesarry state changes to kep the text in the box upon highlighting for every loop
        #and to remove it if the user is not hovering over it
        #In the last case the default text is used indicating what must be done
        if self.hover and self.user_input != "":
            text = self.font.render(self.user_input, True, self.text_colour)
        elif self.hover:
            text = self.font.render("", True, self.text_colour)
        else:
            self.user_input = "" 
            text = self.font.render(self.default_text, True, self.text_colour)
            

        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)
    

    def handle_event(self, event) -> None:

        if event.type == pygame.MOUSEMOTION: #update collide state
            self.hover = True if self.rect.collidepoint(event.pos) else False
            

        elif event.type == KEYDOWN:

            if event.key == K_BACKSPACE: #remove text upon backspace being pressed
                self.user_input = self.user_input[:-1]
            
            elif event.key == K_RETURN: #Upon return set the players name and remove it from the interface list so it wont draw
                GameState.current_player.name = self.user_input
                self.interface.text_boxes.pop(0)
                self.user_input = ""
                
                if all(player.name for player in self.interface.players): #when both players have names start the game
                    self.interface.play_game = True
                
            else:
                self.user_input += event.unicode #add to textbox


 


