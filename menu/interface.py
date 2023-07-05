import pygame
from pygame.locals import *
import colours
import random
from .button import Button

class Menu:
    def __init__(self):
        self._running = True
        

    def on_init(self):
        pygame.init()
        self._running = True

        self.size = self.screen_width, self.screen_height = 800, 600 
        
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_colour = colours.DODGER_BLUE
        self.screen_particles = self._generate_screen_fire()

        self.all_sprites = pygame.sprite.Group()
        self.buttons = self._create_buttons()
    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Menu Example")


    def _create_buttons(self):
        button1 = Button(self.screen_width // 2 - 200, self.screen_height // 2 - 50, 400, 50, "Player V.S. Player", self)
        button2 = Button(self.screen_width // 2 - 200, self.screen_height // 2 + 50, 400, 50, "Player V.S. Computer", self)
        return [button1, button2]
 
    def event(self, event):
        if event.type == QUIT:
            running = False

        for button in self.buttons:
            button.handle_event(event)
        

    def loop(self):
        self.screen.fill(self.screen_colour)
        self._set_screen_particles_to_fire()

        for button in self.buttons:
            button.draw()

        Button.hover = False
        
   
    def render(self):
        pygame.display.flip()
        pygame.time.delay(10)
        self.clock.tick(60)

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


    def _generate_screen_fire(self):
        particles = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 10)
            particles.append([x, y, size])
        return particles

    def _set_screen_particles_to_fire(self):
        for particle in self.screen_particles:
            x, y, size = particle

            # Update particle position
            y -= 1

            # Wrap particle to the bottom if it goes off the screen
            if y < 0:
                y = self.screen_height
                x = random.randint(0, self.screen_width)

            # Draw the particle
            pygame.draw.circle(self.screen, colours.ORANGE, (x, y), size)
            pygame.draw.circle(self.screen, colours.YELLOW, (x, y), size // 2)

            particle[0] = x
            particle[1] = y 
        
          