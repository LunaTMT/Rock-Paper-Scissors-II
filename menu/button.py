import pygame
import colours
import random

class Button:



    def __init__(self, interface, text, x, y, name_state):
        self.interface = interface
        self.screen = interface.screen

        #default rectangle
        self.width = 400
        self.height = 50
        self.rect_x = x
        self.rect_y = y
        self.rect = pygame.Rect(self.rect_x, self.rect_y, self.width, self.height)
        
        #Default appearance
        self.text = text
        self.rect_colour = colours.WHITE
        self.text_colour = self.interface.text_colour

        self.name_state = name_state
        self.hover = False
        

        
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


    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.interface.menu_option =  self.name_state
                self.interface._running = False
                
    


    def get_center_coord(self):
        center_x = (self.interface.screen_width - self.original_width) // 2 
        center_y = (self.interface.screen_height - self.original_height) // 2
        self.rect_x = center_x + self.transpose_x
        self.rect_y = center_y + self.transpose_y
        


