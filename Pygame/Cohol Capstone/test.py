import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


class Line:
    def __init__(self, start_pos, screen_size):
        self.start_pos = start_pos
        self.screen_size = screen_size
        self.angle = 0
        self.length = 0

    def draw(self, surface):
        end_pos = (
            self.start_pos[0] + self.length * math.cos(self.angle),
            self.start_pos[1] + self.length * math.sin(self.angle),
        )
        pygame.draw.line(surface, BLACK, self.start_pos, end_pos, 2)

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 2 * math.pi  # Ensure angle remains within [0, 2*pi]

    def is_clicked(self, mouse_pos):
        end_pos = (
            self.start_pos[0] + self.length * math.cos(self.angle),
            self.start_pos[1] + self.length * math.sin(self.angle),
        )
        distance_to_start = math.dist(self.start_pos, mouse_pos)
        distance_to_end = math.dist(end_pos, mouse_pos)
        return abs(distance_to_start + distance_to_end - self.length) < 5


lines = []
dragging = None
offset = None

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                clicked_line = next(
                    (line for line in lines if line.is_clicked(event.pos)), None
                )
                if clicked_line is not None:
                    dragging = clicked_line
                    offset = (
                        event.pos[0] - dragging.start_pos[0],
                        event.pos[1] - dragging.start_pos[1],
                    )
                else:
                    line = Line(event.pos, size)
                    lines.append(line)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = None
                offset = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging is not None and offset is not None:
                dragging.rotate(event.rel[0] * 0.01)

    screen.fill(WHITE)

    for line in lines:
        line.length = size[0]  # Update the length every frame
        line.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
