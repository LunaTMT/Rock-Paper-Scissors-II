import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

input_text = ""
input_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_active = not input_active
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if input_active:
                    input_text += event.unicode

    screen.fill((255, 255, 255))
    
    if input_active:
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 380, 40), 2)

    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (20, 20))

    pygame.display.update()
    clock.tick(30)
