import pygame

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Variables for tracking mouse clicks
click_counter = 0
start_pos = None

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_counter == 0:
                # Store the start position of the line
                start_pos = event.pos
                click_counter += 1
            elif click_counter == 1:
                # Draw the line from the start position to the end position
                end_pos = event.pos
                pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)
                # Reset click counter
                click_counter = 0
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate to 60 frames per second
    clock.tick(60)

pygame.quit()
