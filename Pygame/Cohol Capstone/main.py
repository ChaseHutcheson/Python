# main.py
import pygame
from settings import Settings
from logic import distance, snapLines

# Program Setup
pygame.init()

# Settings
settings = Settings((1280, 720), (25, 25, 25))

# Screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Circuit Simulator")

# Line Drawing
lines = []
line_start_pos = None
click_counter = 0
clock = pygame.time.Clock()
running = True

while running:
    # GAME LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_counter == 0:
                line_start_pos = pygame.mouse.get_pos()
                click_counter += 1
            elif click_counter == 1:
                line_end_pos = pygame.mouse.get_pos()

                # Snap the line end to nearby lines if applicable
                closest_end, _ = snapLines(lines, line_end_pos)
                if closest_end is not None:
                    line_end_pos = closest_end

                lines.append((line_start_pos, line_end_pos))
                click_counter = 0

    # RENDER GAME
    screen.fill(settings.screen_color)

    # Line Preview
    if click_counter == 1:
        line_end_pos = pygame.mouse.get_pos()

        # Snap the line end to nearby lines if applicable
        closest_end, _ = snapLines(lines, line_end_pos)
        if closest_end is not None:
            print("Closest End:", closest_end)
            line_end_pos = closest_end

        pygame.draw.line(screen, (155, 155, 155), line_start_pos, line_end_pos, 2)

    for line in lines:
        pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
