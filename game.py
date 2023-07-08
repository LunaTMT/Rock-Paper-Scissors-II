import pygame
from pygame.locals import *
import assets.colours as colours
import random
from menu_button import MenuButton
from player import Player
from gamestate import GameState
from textbox import TextBox

class Game:
    def __init__(self):
        self._running = True
        self.size = self.screen_width, self.screen_height = 800, 600 

        self.current_button = None
        self.current_player = None

    def on_init(self):
        pygame.init()
        self._running = True

        self.base_menu = True

        self.title_font = pygame.font.Font("assets/fonts/title_font.ttf", 65)
        self.text_colour = colours.WHITE

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_colour = colours.DODGER_BLUE
        self.screen_particles = self._generate_screen_fire()
        
        screen_rect = self.screen.get_rect()
        self.center_x = screen_rect.centerx
        self.center_y = screen_rect.centery
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.all_sprites = pygame.sprite.Group()

        self.players = []
        self.rectangles = [] 
        self.text_boxes = []
        self.buttons = self.create_menu_buttons()
    


        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Rock Paper Scissors")



    def event(self, event):
        if event.type == QUIT:
            self._running = False

        for button in self.buttons:
            button.handle_event(event)

        print(self.text_boxes)
        for textbox in self.text_boxes:
            textbox.handle_event(event)
        
        
  
    def loop(self):
        if self.base_menu:
            #Button collision state
            collision_state = any(buttons.hover for buttons in self.buttons)
            self.screen_colour = colours.FIREBRICK if collision_state else colours.DODGER_BLUE

        self.screen.fill(self.screen_colour)
        self._set_screen_particles_to_fire()

        #Main menu title
        self.title_surface = self.title_font.render('Rock Paper Scissors', True, self.text_colour)
        self.screen.blit(self.title_surface, (100, 100))
    
        for button in self.buttons:
            button.draw()

        for textbox in self.text_boxes:
            textbox.draw()

        #Once we have our players initialised, but they do not have a set name
       
        
        
   
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
        

    def get_players(self):
        self.buttons = []
        self.base_menu = False
        if self.current_button == "PVP":
            self.players = [Player(self), Player(self)]
            self.current_player = self.players[0]

            name_input = TextBox(self, 0, 0, 400, 50)
            name_input.center_box()
            self.text_boxes.append(name_input)
      
        else:
            print("Getting player and AI")

    def create_menu_buttons(self):
        PVP_button = MenuButton(self, 0, 0, 400, 50, "Player V.S. Player", "PVP", self.get_players)
        PVP_button.center_button()
        PVP_button.transpose(0, -50)

        
        PVC_button = MenuButton(self, 0, 0, 400, 50, "Player V.S. Computer", "PVC", self.get_players)
        PVC_button.center_button()
        PVC_button.transpose(0, 50)
        return [PVP_button, PVC_button]


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
        
    def get_next_player(self):
        GameState.turn += 1
        self.current_player = self.players[GameState.turn % 2]
