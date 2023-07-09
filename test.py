import pygame

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the rectangle dimensions
rect_width = 200
rect_height = 150

# Set the corner radius
corner_radius = 20

# Create a rectangle surface
rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)

# Set the color for the surface
rect_color = (255, 0, 0)

# Draw a rounded rectangle on the surface
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    for i in range(corner_radius):
        pygame.draw.circle(surface, color, (rect.left + corner_radius + i, rect.top + corner_radius),
                           corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - i, rect.top + corner_radius),
                           corner_radius)
        pygame.draw.circle(surface, color, (rect.left + corner_radius + i, rect.bottom - corner_radius),
                           corner_radius)
        pygame.draw.circle(surface, color, (rect.right - corner_radius - i, rect.bottom - corner_radius),
                           corner_radius)

# Draw the rounded rectangle on the rectangle surface
draw_rounded_rect(rect_surface, rect_color, rect_surface.get_rect(), corner_radius)

# Blit the rectangle surface onto the screen at a specific position
rect_x = 300
rect_y = 200
screen.blit(rect_surface, (rect_x, rect_y))

# Update the display
pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
