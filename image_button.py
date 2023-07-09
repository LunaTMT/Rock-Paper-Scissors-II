import pygame
from gamestate import GameState

class ImageButton():

    def __init__(self, interface, image, highlight_image, x, y, name_state, function):
        self.interface = interface
        self.screen = interface.screen
        self.image = image
        self.highlight_image = highlight_image
        
    
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()

        self.name_state = name_state
        self.function = function 
        self.hover = False

        self._set_rect()

        

    def draw(self):

        if self.hover:
            self.screen.blit(self.highlight_image, (self.x, self.y))
        else:
            self.screen.blit(self.image, (self.x, self.y))

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                GameState.get_next_player()
                self.function(self.name_state) 
               

    def _set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def place_at_bottom(self):
        self.y = self.interface.screen_height - self.height - 10
        self._set_rect()

