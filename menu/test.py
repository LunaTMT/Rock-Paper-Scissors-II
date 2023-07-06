import pygame
import sys
import random

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 200))
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Define text properties
text = "Fire"
font = pygame.font.Font(None, 80)

# Define particle properties
particles = []
num_particles = 500

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Generate particles
    if len(particles) < num_particles:
        particles.append([random.randint(0, screen.get_width()), screen.get_height()])

    # Update and draw particles
    for particle in particles:
        particle[0] += random.randint(-1, 1)
        particle[1] -= random.randint(1, 5)
        pygame.draw.circle(screen, random.choice([RED, ORANGE]), particle, random.randint(1, 3))

    # Render and draw text
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)
