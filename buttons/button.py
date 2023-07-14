import pygame
import assets.colours as colours

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


    def _set_rect(self) -> None:
        """
        This function simple creates a new instance of the button rectangle with the current obj attributes
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
   
    def draw(self) -> None:
        """
        Draws the button rectangle on screen
        """
        pygame.draw.rect(self.screen, self.rect_colour, self.rect, border_radius = 20)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_colour)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

    def handle_event(self, event) -> None:
        """
        handles the events for all button objects
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.interface.current_button = self.name_state
                self.function()               
                
    def center_button(self) -> None:
        """
        This function centers the button, updates its coordinates and calls the method update the rectangle but recreating it
        """
        center_x = (self.screen_width - self.width) // 2 
        center_y = (self.screen_height - self.height) // 2
        self.x = center_x
        self.y = center_y 
        self._set_rect()
        
    def transpose(self, x=0, y=0) -> None:
        """
        This function will transpose the current button position by the 2 aurgments passed into the function
        """
        self.x += x
        self.y += y
        self._set_rect()

    def place_at_bottom(self) -> None:
        """
        This function simply changes the y coordinate of the given button and places it at the bottom 
        """
        self.y = self.interface.screen_height - self.height - 30
        self._set_rect()
    
    def move_to_center(self) -> None:
        """
        Sets obj x and y to center
        """

        while self.x != self.center_x:
            if self.x < self.center_x:
                self.x += 1
            else:
                self.x -= 1

            self.draw()

