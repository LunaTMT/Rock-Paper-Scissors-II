import pygame
import assets.colours as colours

import gamestate

class Button:

    def __init__(self, interface, x, y, width, height, text, name_state, function):
        self.screen = interface.screen
        self.screen_width = interface.screen_width
        self.screen_height =  interface.screen_height

        #default rectangle
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self._set_rect()
        
        #Default appearance
        self.text = text
        self.rect_colour = colours.WHITE
        self.text_colour = colours.WHITE

        self.name_state = name_state
        self.function = function
        self.hover = False


    def _set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
   
    def draw(self):
        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.interface.current_button = self.name_state
                self.function()
                
                
    def center_button(self):
        center_x = (self.screen_width - self.width) // 2 
        center_y = (self.screen_height - self.height) // 2
        self.x = center_x
        self.y = center_y 
        self._set_rect()
        
    def transpose(self, x, y):
        self.x += x
        self.y += y
        self._set_rect()
