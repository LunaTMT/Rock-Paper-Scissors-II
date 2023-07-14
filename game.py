import pygame
import random
import time

from pygame.locals import *

import assets.colours as colours
from buttons.menu_button import MenuButton
from buttons.image_button import ImageButton
from players.player import Player
from gamestate import GameState
from textbox import TextBox
from players.ai import Ai
from gamestate import GameState


class Game:
    def __init__(self) -> None:
        pygame.display.set_caption("Rock Paper Scissors")
        self._running = True
        self.size = self.screen_width, self.screen_height = 800, 600 

        self.base_menu = True
        self.players_set = False
        self.play_game = False
        self.show_countdown = False
        self.show_winner = False


    def on_init(self) -> None:
        pygame.init()
        self._running = True

        self.initialise_images()
    
        self.title_font = pygame.font.Font("assets/fonts/title.ttf", 65)
        self.countdown_font = pygame.font.Font(None, 60)
        self.scoreboard_font = pygame.font.Font("assets/fonts/scoreboard.ttf", 50)
        self.text_colour = colours.WHITE
        
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.screen_colour = colours.DODGER_BLUE
        self.screen_particles = self.generate_screen_particles()
        
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
        
        self.countdown = {3: "Rock",
                          2: "Paper",
                          1: "Scissors"}

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
            #Button collision state - 
            #Used to change the colour of the background when the player highlights over any button
            collision_state = any(buttons.hover for buttons in self.buttons)
            self.screen_colour = colours.FIREBRICK if collision_state else colours.DODGER_BLUE

        #fill screen with the designated colour above and create the fire particles
        self.screen.fill(self.screen_colour)
        self.draw_screen_particle()


        #Main menu title
        self.draw_title(self.title_font, "Rock Paper Scissors", 1, 0.5)
        
    
        for button in self.buttons:
            button.draw()

        for textbox in self.text_boxes:
            textbox.draw()


        #So long has the players have been set such that they have been instantiated and have a name, we will draw their choice and score
        if self.players_set and all(player.name for player in GameState.players):
            for player in GameState.players:
                player.draw_score()
                player.draw_choice()
                
                 
        #When the game itself actually begins
        if self.play_game:
           

            #Until both players made a choice we want to keep displaying the flash to feign the opponent making a decision
            if not all(player.choice for player in GameState.players):
                self.generate_flashing_choices()
                
            
            #used to make following code clearer
            current_player = GameState.current_player 

            #Until it is the Ai's turn 
            if isinstance(current_player, Ai) and current_player.choice == "":
                current_player.get_choice()
                GameState.get_next_player()
                
                self.buttons = [] 
                self.play_game = False
                self.show_countdown = True  #State transition"""

                #The start time is used between state transition 
                #for there to be a delay of 3 seconds before the next state
                self.start_time = time.time() 

            else:
                if len(self.buttons) < 3:
                    self.generate_choice_buttons()
            

        #The following is self-explanatory and does not need explanation
        if self.show_countdown:
            self.generate_flashing_choices()
            self.generate_flashing_choices(transpose_y = 205)
            self.draw_countdown()

        if self.show_winner:
            self.get_win_state()
            self.draw_title(self.title_font, self.win_state, 1, 1.4)
           
            



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
        


    def initialise_images(self) -> None:
        """"
        Here we initialise all the Rock Paper Scissor images to be used. 
        The golden images are created from the imported ones which are to be used when the button is hovered over.
        """

        # I am aware that the rock image is slightly smaller and is a little bit distracting with flashing between all other options
        # if the rock is changed with the new_rock of a different scaled size, the program just breaks upon choice selection for some reason
        # unfortunately, I could not figure out why this was the case
        #self.rock_img = pygame.image.load("assets/images/newly_scaled_rock.png")

        self.rock_img = pygame.image.load("assets/images/rock.png")
        self.paper_img = pygame.image.load("assets/images/paper.png") 
        self.scissors_img = pygame.image.load("assets/images/scissors.png")


        self.rock_img = self.resize_image(self.rock_img, 0.3)
        self.paper_img = self.resize_image(self.paper_img, 0.3)
        self.scissors_img = self.resize_image(self.scissors_img, 0.3)

        self.golden_rock_img = self.create_golden_image(self.rock_img)
        self.golden_paper_img = self.create_golden_image(self.paper_img)
        self.golden_scissors_img = self.create_golden_image(self.scissors_img)

        #Array is used for the flashing between all images
        self.RPS_images = [self.rock_img , self.paper_img, self.scissors_img]

        #They are all the same size 
        img_size = self.rock_img.get_rect()

        self.choice_img_center_x = (self.screen_width - img_size.width) // 2
        self.choice_img_center_y = (self.screen_height - img_size.height) // 2

        self.current_image = 0

    def resize_image(self, image, percentage) -> pygame.surface:
        """Resizes a given image"""
        width, height = image.get_size()
        return pygame.transform.scale(image, (width * percentage, height * percentage))
    
    def create_golden_image(self, image) -> pygame.image:
        """
        Changes the hue of the image passed in to golden
        """
        # Create a copy of the image to modify

        image = image.copy()
        # Iterate over each pixel in the image
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))

                # Apply goldish color effect
                r = min(int(r * 2), 255)    # Increase red component
                g = min(int(g * 1.1), 255)  # Increase green component
                b = min(int(b * 0.1), 255)  # Decrease blue component

                image.set_at((x, y), (r, g, b, a))
        return image
    


    def generate_choice_buttons(self) -> None:
        """
        Creates three instances of an image button class and moves them to the bottom.
        
        """
          
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
        
    
        self.buttons += [self.rock, self.paper, self.scissors]
 
    def generate_menu_buttons(self) -> MenuButton:
        """
        This function generates the intial button(s) to be used on the menu
        """
        PCP_button = MenuButton(self, 0, 0, 400, 50, "Player V.S. Computer", "PVC", self.get_players)
        PCP_button.center_button()

        return [PCP_button]

    def generate_flashing_choices(self, transpose_x=0, transpose_y=0) -> None:
        """
        This function blits onto the screen all choices in order such that it 
        appears the opponent is making up their mind what to choice
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.timer

        # Check if it's time to switch the image
        if elapsed_time >= self.delay:
            self.current_image = (self.current_image + 1) % len(self.RPS_images)  # Increment the current image index
            self.timer = pygame.time.get_ticks()  # Reset the timer

        # Display the current image
        self.screen.blit(self.RPS_images[self.current_image], (self.choice_img_center_x + transpose_x,  self.choice_img_center_y + transpose_y))

    def generate_screen_particles(self) -> list[int]:
        """
        generates random particles to be blitted on the screen, x_cord, y_cord and size of particle
        """
        particles = []
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 10)
            particles.append([x, y, size])
        return particles



    def draw_countdown(self) -> None:
        """
        draws a countdown in the center of the screen from 3
        """
        
        elapsed_time = time.time() - self.start_time
        remaining_time = 3 - elapsed_time

        
        if remaining_time > 0:
            self.draw_title(self.scoreboard_font, self.countdown[int(remaining_time) + 1], 1, 1.38 )
        else:
            self.show_countdown = False
            self.show_winner = True
            self.start_time = time.time()

    def draw_screen_particle(self) -> None:
        """
        This function draws the screen particles onto the screen
        """
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

    def draw_title(self, font,  text, x, y) -> None:
        """
        A simple method that will print on the screen a title of given parameters
        """
        title = font.render(text, True, self.text_colour)
        width, height = self.get_title_size(title)
        self.screen.blit(title, self.get_centered_coord(width, height, x, y))



    def get_players(self) -> None:
        """
        This function instantiates two player objects, 
        One player and one Ai opponent

        A texbox obj is created to get the name from the player
        """
        self.buttons = []
        self.base_menu = False
        self.players_set = True

        if self.current_button == "PVC":
            GameState.players = [Player(self), Ai(self)]
            GameState.current_player = GameState.players[0]

            name_input = TextBox(self, 0, 0, 400, 50)
            name_input.center_box()
            self.text_boxes.append(name_input)

    def get_title_size(self, title) -> tuple[int]:
        """
        Gets the height and width of a rect object and returns it
        """
        title_size = title.get_rect()
        return  title_size.width, title_size.height

    def get_centered_coord(self, width, height, x_tranpose=1, y_transpose=1 ) -> int:
        """
        Gets the center coordinates based on an image or rect otherwise the image will be slightly off 
        when using self.center_x, self.center_y
        """
        center_x = (self.screen_width - width) // 2
        center_y = (self.screen_height - height) // 2
        return center_x * x_tranpose, center_y * y_transpose

    def get_win_state(self) -> None:
        """
        This function finds out whether the player has won or lost
        """
        self.win_state = "" 
        p1, p2 = GameState.players

        if p1.choice == p2.choice:
            self.win_state =  "Draw"
        elif self.rules[p1.choice] == p2.choice:
            self.win_state =  "Win"
        else:
            self.win_state =  "You loose"

        elapsed_time = time.time() - self.start_time
        remaining_time = 3 - elapsed_time
        
        if remaining_time > 0:
            pass
        else:
            self.show_winner = False
            self.players_set = True
            self.play_game = True

            self.update_score()

            for player in GameState.players:
                player.choice = ""



    def update_score(self) -> None:
        """
        This funciton updates the players score once the win_state has been determined
        """
        if self.win_state == "Win":
            GameState.players[0].score += 1
        elif self.win_state == "You loose":
            GameState.players[1].score += 1
        else:
            pass
