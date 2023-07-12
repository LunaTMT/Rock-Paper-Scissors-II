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
from gamestate import GameState
import time

class Game:
    def __init__(self):
        pygame.display.set_caption("Rock Paper Scissors")
        self._running = True
        self.size = self.screen_width, self.screen_height = 800, 600 

        self.base_menu = True
        self.play_game = False
        self.show_countdown = False
        self.show_winner = False
        self.players_set = False

    def on_init(self):
        pygame.init()
        self._running = True

        self.initialise_images()
    
        self.title_font = pygame.font.Font("assets/fonts/title_font.ttf", 65)
        self.sub_heading_font = pygame.font.Font(None, 32)
        self.countdown_font = pygame.font.Font(None, 100)
        self.text_colour = colours.WHITE
        

        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_colour = colours.DODGER_BLUE
        self.screen_particles = self._generate_screen_particles()
        
        self.all_sprites = pygame.sprite.Group()

        screen_rect = self.screen.get_rect()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.center_x = screen_rect.centerx
        self.center_y = screen_rect.centery

        self.players = []
        self.text_boxes = []
        self.buttons = self.generate_menu_buttons()

        self.rules = {  "Rock"    : "Scissors",            
                        "Paper"    : "Rock",           
                        "Scissors" : "Paper"}    

        self.clock = pygame.time.Clock()
        self.timer = pygame.time.get_ticks()
        self.delay = 400
        self.countdown_duration = 3  # 3 seconds
        
        

        


    def event(self, event):
        if event.type == QUIT:
            self._running = False

        for button in self.buttons:
            button.handle_event(event)

        for textbox in self.text_boxes:
            textbox.handle_event(event)
    
        
        
  
    def loop(self):
        if self.base_menu:
            
            #Button collision state - is used to change the colour of the backfground when the player highlights over any button
            collision_state = any(buttons.hover for buttons in self.buttons)
            self.screen_colour = colours.FIREBRICK if collision_state else colours.DODGER_BLUE

        #fill screen with the designated colour above and create the fire particles
        self.screen.fill(self.screen_colour)
        self._set_screen_particle()


        #Main menu title
        self.draw_title(self.title_font, "Rock Paper Scissors", 1, 0.5)
        
    
        for button in self.buttons:
            button.draw()

        for textbox in self.text_boxes:
            textbox.draw()

        if self.players_set:
            for player in GameState.players:
                player.draw_choice() 

    
        if self.play_game:

            if not all(player.choice for player in GameState.players):
                self._generate_flashing_choices()
                
            current_player = GameState.current_player #used to make following code clearer
            current_player.draw_info()
    
            if isinstance(current_player, Ai):
                self.buttons = [] #remove buttons from screen

                #only want to get the choice once
                if not current_player.choice:
                    current_player.get_choice()
                    
                    self.play_game = False
                    self.show_countdown = True
                    self.start_time = time.time()
                
            else:
                self.draw_choice_buttons()
            
        if self.show_countdown:
            self._generate_flashing_choices()
            self.draw_countdown()

        if self.show_winner:
            self.check_winner()

 
            
            

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
        


    def initialise_images(self):
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

        #They are all the same size 
        img_size = self.rock_img.get_rect()

        self.choice_img_center_x = (self.screen_width - img_size.width) // 2
        self.choice_img_center_y = (self.screen_height - img_size.height) // 2


        self.current_image = 0

    
    def generate_menu_buttons(self):
        PCP_button = MenuButton(self, 0, 0, 400, 50, "Player V.S. Computer", "PVC", self.get_players)
        PCP_button.center_button()

        return [PCP_button]

    def _generate_flashing_choices(self):
    
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer

        # Check if it's time to switch the image
        if elapsed_time >= self.delay:
            self.current_image = (self.current_image + 1) % len(self.RPS_images)  # Increment the current image index
            self.timer = pygame.time.get_ticks()  # Reset the timer

        # Display the current image
        self.screen.blit(self.RPS_images[self.current_image], (self.choice_img_center_x,  self.choice_img_center_y))

    def _generate_screen_particles(self):
        particles = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 10)
            particles.append([x, y, size])
        return particles

    def _set_screen_particle(self):
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
    

    def draw_grid(self):
        pygame.draw.line(self.screen, colours.BLACK, (0, 170), (self.screen_width, 170), 5)
        pygame.draw.line(self.screen, colours.BLACK, (self.center_x, 170), (self.center_x, self.screen_height), 5)

    def draw_title(self, font,  text, x, y):
        title = font.render(text, True, self.text_colour)
        width, height = self.get_title_size(title)
        self.screen.blit(title, self.get_centered_coord(width, height, x, y))

    def draw_countdown(self):
        
        elapsed_time = time.time() - self.start_time
        remaining_time = 3 - elapsed_time
        
        
        if remaining_time > 0:
            print(True)
            self.draw_title(self.countdown_font, str(int(remaining_time) + 1), 1, 1.43 )
        else:
            self.show_countdown = False
            self.show_winner = True
  
    def draw_choice_buttons(self):
        self.rock = ImageButton(self, 
                                   self.rock_img, 
                                   self.golden_rock_img, 
                                   self.choice_img_center_x * 0.5, 0, 
                                   "Rock", 
                                   GameState.set_current_choice)
                
        self.paper = ImageButton(self, 
                            self.paper_img, 
                            self.golden_paper_img, 
                            self.choice_img_center_x * 1, 0, 
                            "Paper", 
                            GameState.set_current_choice)
        
        self.scissors = ImageButton(self, 
                                self.scissors_img, 
                                self.golden_scissors_img, 
                                self.choice_img_center_x * 1.5, 0, 
                                "Scissors", 
                                GameState.set_current_choice)
    
        self.rock.place_at_bottom()
        self.paper.place_at_bottom()
        self.scissors.place_at_bottom()
        
        if len(self.buttons) < 3:
            self.buttons += [self.rock, self.paper, self.scissors]



    def get_players(self):
        self.buttons = []
        self.base_menu = False
        
        if self.current_button == "PVC":
            GameState.players = [Player(self), Ai(self)]
            GameState.current_player = GameState.players[0]
            self.players_set = True

            name_input = TextBox(self, 0, 0, 400, 50)
            name_input.center_box()
            self.text_boxes.append(name_input)

    def get_title_size(self, title):
        title_size = title.get_rect()
        return  title_size.width, title_size.height

    def get_centered_coord(self, width, height, x_tranpose=1, y_transpose=1 ):
        center_x = (self.screen_width - width) // 2
        center_y = (self.screen_height - height) // 2
        return center_x * x_tranpose, center_y * y_transpose
        



    def check_winner(self):

        p1, p2 = GameState.players

        if p1.choice == p2.choice:
            self.draw_title(self.title_font, "Draw", 1, 1.4)

        elif self.rules[p1.choice] == p2.choice:
            self.draw_title(self.title_font, "Win", 1, 1.4)
        else:
            self.draw_title(self.title_font, "You loose", 1, 1.4)

  
  