from button import Button
import assets.colours as colours

import pygame

class MenuButton(Button):
    
    def __init__(self, interface, x, y, width, height, text, name_state, function):
        super().__init__(interface, x, y, width, height, text, name_state, function)
        self.interface = interface

    def draw(self):
        if self.hover:
            self.rect_colour = colours.GOLD
            self.text_colour = colours.BLACK
        
        else:
            #If the current button being drawn is not(!) the one being hovered over,
            # then its colours must match the background 
            if self.interface.screen_colour == colours.FIREBRICK:
                self.rect_colour = colours.FIREBRICK_2 
                self.interface.text_colour = colours.BLACK 
            else:
                self.rect_colour = colours.DODGER_BLUE_2
                self.interface.text_colour = colours.WHITE 

        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.interface.text_colour)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)