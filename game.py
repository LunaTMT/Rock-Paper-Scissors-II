import pygame
from pygame.locals import *
import assets.colours as colours
import random
from menu_button import MenuButton
from image_button import ImageButton
from button import Button
from player import Player
from gamestate import GameState
from textbox import TextBox
from ai import Ai

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
        self.sub_tiltes_font = pygame.font.Font(None, 32)


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



        self.rock_img = pygame.image.load("assets/images/rock.png")
        self.paper_img = pygame.image.load("assets/images/paper.png") 
        self.scissors_img = pygame.image.load("assets/images/scissors.png")

        self.rock_img = self.resize_image(self.rock_img, 0.3)
        self.paper_img = self.resize_image(self.paper_img, 0.3)
        self.scissors_img = self.resize_image(self.scissors_img, 0.3)

        self.golden_rock_img = self.create_golden_image(self.rock_img)
        self.golden_paper_img = self.create_golden_image(self.paper_img)
        self.golden_scissors_img = self.create_golden_image(self.scissors_img)



        self.RPS_images = [self.rock_img , self.paper_img, self.scissors_img]

        self.current_image = 0
        self.timer = pygame.time.get_ticks()
        self.delay = 400

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Rock Paper Scissors")



    def event(self, event):
        if event.type == QUIT:
            self._running = False

        for button in self.buttons:
            button.handle_event(event)

        for textbox in self.text_boxes:
            textbox.handle_event(event)

        for rect in self.rectangles:
            rect.handle_event(event)
        
        
  
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
            print(len(self.buttons))
            button.draw()

        for textbox in self.text_boxes:
            textbox.draw()

        if self.players != [] and all(player.name for player in self.players):
            
            pygame.draw.line(self.screen, colours.BLACK, (0, 170), (self.screen_width, 170), 5)
            pygame.draw.line(self.screen, colours.BLACK, (self.center_x, 170), (self.center_x, self.screen_height), 5)


            p1_name = self.sub_tiltes_font.render(self.players[0].__str__(), True, self.text_colour)
            self.screen.blit(p1_name, (10, 180))
            self._generate_flashing_choices(self.center_x * 0.35 ,self.center_y)

            rock = ImageButton(self, self.rock_img, self.golden_rock_img, self.center_x * 0.01, 0, "rock", None)
            paper = ImageButton(self, self.paper_img, self.golden_paper_img, self.center_x * 0.67, 0, "paper", None)
            scissors = ImageButton(self, self.scissors_img, self.golden_scissors_img, self.center_x * 0.34, 0, "scissors", None)
        
            rock.place_at_bottom()
            paper.place_at_bottom()
            scissors.place_at_bottom()
            
            if len(self.buttons) < 3:
                self.buttons += [rock, paper, scissors]


            p2_name = self.sub_tiltes_font.render(self.players[1].__str__(), True, self.text_colour)
            self.screen.blit(p2_name, (self.center_x + 10, 180))
            self._generate_flashing_choices(self.center_x * 1.35 ,self.center_y)
            
            
            

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
        if self.current_button == "PVC":
            self.players = [Player(self), Ai(self)]
            self.current_player = self.players[0]

            name_input = TextBox(self, 0, 0, 400, 50)
            name_input.center_box()
            self.text_boxes.append(name_input)
            
      

    def create_menu_buttons(self):
        PCP_button = MenuButton(self, 0, 0, 400, 50, "Player V.S. Computer", "PVC", self.get_players)
        PCP_button.center_button()

        return [PCP_button]


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
        
    def _generate_flashing_choices(self, x , y):
    
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer

        # Check if it's time to switch the image
        if elapsed_time >= self.delay:
            self.current_image = (self.current_image + 1) % len(self.RPS_images)  # Increment the current image index
            self.timer = pygame.time.get_ticks()  # Reset the timer

        # Display the current image
        self.screen.blit(self.RPS_images[self.current_image], (x, y))


    def get_next_player(self):
        GameState.turn += 1
        self.current_player = self.players[GameState.turn % 2]

    def resize_image(self, image, percentage):
        width, height = image.get_size()
        return pygame.transform.scale(image, (width * percentage, height * percentage))
    
    def create_golden_image(self, image):
        # Create a copy of the image to modify

        image = image.copy()
        # Iterate over each pixel in the image
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))

                # Apply goldish color effect
                r = min(int(r * 2), 255)  # Increase red component
                g = min(int(g * 1.1), 255)  # Increase green component
                b = min(int(b * 0.1), 255)  # Decrease blue component

                image.set_at((x, y), (r, g, b, a))
        return image