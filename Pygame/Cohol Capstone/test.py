import pygame
import sys

lines = []
current_line = None


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255), self.start, self.end, 2)

    def calculate_extended_points(self, screen_size):
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]

        if dx != 0:
            slope = dy / dx
            y_intercept = self.start[1] - slope * self.start[0]

            # Calculate new x and y for the left and right edges of the screen
            x_left = 0
            y_left = y_intercept

            x_right = screen_size[0]
            y_right = slope * x_right + y_intercept

            # Check if the line intersects with the top or bottom before it hits the left or right
            y_top = 0
            x_top = (y_top - y_intercept) / slope if slope != 0 else self.start[0]

            y_bottom = screen_size[1]
            x_bottom = (y_bottom - y_intercept) / slope if slope != 0 else self.start[0]

            new_points = [
                (x_left, y_left),
                (x_right, y_right),
                (x_top, y_top),
                (x_bottom, y_bottom),
            ]
            new_points = [
                (x, y)
                for x, y in new_points
                if 0 <= x <= screen_size[0] and 0 <= y <= screen_size[1]
            ]
            new_points.sort(
                key=lambda point: (point[0] - self.start[0]) ** 2
                + (point[1] - self.start[1]) ** 2
            )

            return new_points[0], new_points[-1]
        else:
            return (self.start[0], 0), (self.start[0], screen_size[1])


def main():
    global lines, current_line
    pygame.init()

    # Set the dimensions of the window
    screen = pygame.display.set_mode((800, 600))
    screen_size = screen.get_size()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the left mouse button
                    if current_line is None:  # If no line is currently being drawn
                        current_line = Line(event.pos, event.pos)
                    else:  # If a line is currently being drawn
                        current_line.end = event.pos
                        extended_start, extended_end = (
                            current_line.calculate_extended_points(screen_size)
                        )
                        extended_line = Line(extended_start, extended_end)
                        lines.append(extended_line)
                        current_line = None
            elif event.type == pygame.MOUSEMOTION:
                if current_line is not None:  # If a line is currently being drawn
                    current_line.end = event.pos

        # Fill the screen with a color
        screen.fill((0, 0, 0))

        # Draw all lines
        for line in lines:
            line.draw(screen)
        if current_line is not None:
            current_line.draw(screen)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
