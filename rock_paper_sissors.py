import pygame
from pygame.locals import *
import colours 



class RockPaperScissors:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 800, 600 


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen.fill(colours.WHITE) 
        self.all_sprites = pygame.sprite.Group()
        self._running = True

 
        pygame.display.set_caption("Menu Example")

 
    def event(self, event):
        pass

    def loop(self):
        pass

    def render(self):
        pass

    def cleanup(self):
        pygame.quit()

    def run(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        self.cleanup()

