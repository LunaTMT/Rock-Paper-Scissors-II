import pygame
import colours
import random

class Button:

    hover = False

    def __init__(self, x, y, width, height, text, interface):
        self.interface = interface
        self.screen = interface.screen

        self.rect = pygame.Rect(x, y, width, height)
        self.rect_x = x
        self.rect_y = y
        self.rect_width = width
        self.rect_height = height
        
        self.text = text
        self.rect_colour = colours.WHITE
        self.text_colour = colours.DODGER_BLUE_2

        
        
        self.animation_delay = 0  # Delay in milliseconds
        self.color_animation_timer = 0
        self.fire_colour_cycle = [colours.RED, colours.ORANGE, colours.YELLOW]

        self.hover = False



        
    def draw(self):
    
        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)


    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                Button.hover = True
            
                self.rect_colour = colours.GOLD
                self.text_colour = colours.BLACK

                self.interface.screen_colour = colours.FIREBRICK
            elif Button.hover:
                if self.interface.screen_colour == colours.FIREBRICK:
                    self.rect_colour = colours.FIREBRICK_2 
                else:
                    self.rect_colour = colours.DODGER_BLUE_2
 


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"Button '{self.text}' clicked!")
    


