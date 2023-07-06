import pygame
from pygame.locals import *
import colours
import random
from .button import Button

class Menu:
    def __init__(self):
        self._running = True
        self.size = self.screen_width, self.screen_height = 800, 600 
        self.center_x = (self.screen_width - 400) // 2
        self.center_y = (self.screen_height - 50) // 2
        self.menu_option = None
        self.text_colour = colours.WHITE


    def on_init(self):
        pygame.init()
        self._running = True

        self.title_font = pygame.font.Font("fonts/title_font.ttf", 65)
        self.title_text = "Rock Paper Scissors"
        

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_colour = colours.DODGER_BLUE
        self.screen_particles = self._generate_screen_fire()

        self.all_sprites = pygame.sprite.Group()
        self.buttons = self._create_buttons()
    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Menu Example")


    def _create_buttons(self):
        button1 = Button(self, "Player V.S. Player",   self.center_x, self.center_y - 50, "PVP")
        button2 = Button(self, "Player V.S. Computer", self.center_x, self.center_y + 50, "PVC")
        return [button1, button2]
 
    def event(self, event):
        if event.type == QUIT:
            self._running = False

        for button in self.buttons:
            button.handle_event(event)
        
  

    def loop(self):
        
        collision_state = any(buttons.hover for buttons in self.buttons)
        if collision_state:
            self.screen_colour = colours.FIREBRICK
           
        else: 
            self.screen_colour = colours.DODGER_BLUE
        
        self.screen.fill(self.screen_colour)

        self._set_screen_particles_to_fire()

        self.title_surface = self.title_font.render(self.title_text, True, self.text_colour)
        self.screen.blit(self.title_surface, (self.center_x - 85, self.center_y - 165))
        
        for button in self.buttons:
            button.draw()
        
   
    def render(self):
        pygame.display.flip()
        pygame.time.delay(10)
        self.clock.tick(60)

    def cleanup(self):
        pygame.quit()

    def run(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()

        self.cleanup()
        return self.menu_option

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
        
