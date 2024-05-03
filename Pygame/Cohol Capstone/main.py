import pygame
import math
import sys

# Pygame initialization
pygame.init()

# Window settings
WIDTH, HEIGHT = 900, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DRAWING_BACKGROUND = (50, 50, 50)
TOOLBAR_BACKGROUND = (70, 70, 70)
BUTTON_OUTLINE = (100, 100, 100)
BUTTON_BACKGROUND = (150, 150, 150)
GRAY = (200, 200, 200)
MIRROR = (173, 216, 230)

# Toolbar settings
TOOLBAR_WIDTH = 150
TOOLBAR_HEIGHT = win.get_height()
TOOLBAR_X = 0
TOOLBAR_Y = 0

# Define the size and position of the buttons
BUTTON_WIDTH = 130
BUTTON_HEIGHT = 50
BUTTON_X = (TOOLBAR_WIDTH - BUTTON_WIDTH) / 2

# Drawing settings
drawing = False
mode = "light"

# Create a font object
font = pygame.font.Font(None, 24)

# Global variables
lines = []
current_line = None

# Font
FONT = pygame.font.Font(None, 32)


# Utils
def intersect(line1, line2):
    if isinstance(line1, Light):
        x1, y1 = line1.start_pos
        x2, y2 = line1.end_pos
    elif isinstance(line1, Mirror):
        x1, y1 = line1.start_pos
        x2, y2 = line1.end_pos

    if isinstance(line2, Light):
        x3, y3 = line2.start_pos
        x4, y4 = line2.end_pos
    elif isinstance(line2, Mirror):
        x3, y3 = line2.start_pos
        x4, y4 = line2.end_pos

    # Calculate the denominators of the equations
    den1 = (x1 - x2) * (y3 - y4)
    den2 = (y1 - y2) * (x3 - x4)
    denominator = den1 - den2

    # If the denominator is 0, the lines are parallel and don't intersect
    if denominator == 0:
        return None

    # Calculate the numerators of the equations
    num1 = x1 * y2 - y1 * x2
    num2 = x3 * y4 - y3 * x4
    numerator_x = num1 * (x3 - x4) - (x1 - x2) * num2
    numerator_y = num1 * (y3 - y4) - (y1 - y2) * num2

    # Calculate the intersection point
    x = numerator_x / denominator
    y = numerator_y / denominator

    # Check if the intersection point is within the bounds of both lines
    if (
        min(x1, x2) <= x <= max(x1, x2)
        and min(y1, y2) <= y <= max(y1, y2)
        and min(x3, x4) <= x <= max(x3, x4)
        and min(y3, y4) <= y <= max(y3, y4)
    ):
        return (x, y)

    return None


def check_intersections_and_reflect(lines, mirrors):
    new_lines = []
    for line in lines:
        for mirror in mirrors:
            intersection_point = intersect(line, mirror)
            if intersection_point is not None:
                mirror.reflect(line, new_lines)
                line.update(intersection_point)
    lines.extend(new_lines)


# Classes
class Light:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.dx = self.end_pos[0] - self.start_pos[0]
        self.dy = self.end_pos[1] - self.start_pos[1]
        self.length = math.hypot(self.dx, self.dy)
        self.angle = math.atan2(self.dy, self.dx)

    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255), self.start_pos, self.end_pos, 2)

    def calculate_extended_points(self, screen_size):
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]

        if dx != 0:
            slope = dy / dx
            y_intercept = self.start_pos[1] - slope * self.start_pos[0]

            # Calculate new x and y for the left and right edges of the screen
            x_left = 0
            y_left = y_intercept

            x_right = screen_size[0]
            y_right = slope * x_right + y_intercept

            # Check if the line intersects with the top or bottom before it hits the left or right
            y_top = 0
            x_top = (y_top - y_intercept) / slope if slope != 0 else self.start_pos[0]

            y_bottom = screen_size[1]
            x_bottom = (
                (y_bottom - y_intercept) / slope if slope != 0 else self.start_pos[0]
            )

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
                key=lambda point: (point[0] - self.start_pos[0]) ** 2
                + (point[1] - self.start_pos[1]) ** 2
            )

            return new_points[0], new_points[-1]
        else:
            return (self.start_pos[0], 0), (self.start_pos[0], screen_size[1])

    def update(self, end_pos):
        self.end_pos = end_pos


class Mirror:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.dx = self.end_pos[0] - self.start_pos[0]
        self.dy = self.end_pos[1] - self.start_pos[1]
        self.length = math.hypot(self.dx, self.dy)
        self.angle = math.atan2(self.dy, self.dx)

    def update(self, end_pos):
        self.end_pos = end_pos
        self.dx = self.end_pos[0] - self.start_pos[0]
        self.dy = self.end_pos[1] - self.start_pos[1]
        self.length = math.hypot(self.dx, self.dy)
        self.angle = math.atan2(self.dy, self.dx)

    def draw(self, surface):
        pygame.draw.line(surface, MIRROR, self.start_pos, self.end_pos, 5)

    def reflect(self, light, new_lines):
        # Calculate the angle of incidence
        incidence_angle = light.angle - self.angle

        # Calculate the angle of reflection
        reflection_angle = self.angle - incidence_angle

        # Calculate the new direction of the light
        dx = math.cos(reflection_angle)
        dy = math.sin(reflection_angle)

        # Calculate the intersection point
        intersection_point = intersect(light, self)

        # Create a new light ray starting from the intersection point and add it to the new_lines list
        if intersection_point is not None and light.start_pos != intersection_point:
            new_light = Light(
                intersection_point,
                (
                    intersection_point[0] + dx * light.length,
                    intersection_point[1] + dy * light.length,
                ),
            )
            new_lines.append(new_light)


class Button:
    def __init__(self, x, y, width, height, color, text="", click_action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.click_action = click_action

    def draw(self):
        if self.is_hovered():
            pygame.draw.rect(
                win, BUTTON_OUTLINE, self.rect.inflate(6, 6)
            )  # Draw outline when hovered
        pygame.draw.rect(win, self.color, self.rect)
        if self.text != "":
            font = pygame.font.Font(None, 32)
            text = font.render(self.text, True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            win.blit(text, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self):
        return (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        )

    def click(self):
        if self.click_action is not None:
            self.click_action()


# Button actions
def light_button_action():
    global mode
    mode = "light"
    print("Light Mode Activated!")


def mirror_button_action():
    global mode
    mode = "mirror"
    print("Mirror Mode!")


# Toolbar buttons
toolbar_buttons = [
    Button(
        BUTTON_X,  # Centered horizontally
        HEIGHT // 6 * 1 - BUTTON_HEIGHT // 2,  # Evenly spaced vertically
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_BACKGROUND,
        "Light Mode",
        light_button_action,
    ),
    Button(
        BUTTON_X,  # Centered horizontally
        HEIGHT // 6 * 2 - BUTTON_HEIGHT // 2,  # Evenly spaced vertically
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_BACKGROUND,
        "Mirror Mode",
        mirror_button_action,
    ),
]

lines = []
current_line = None


def main():
    global lines, current_line
    pygame.init()

    screen_size = win.get_size()

    mirrors = []
    new_lines = []

    # Game loop
    while True:
        check_intersections_and_reflect(lines, mirrors)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if not (
                        TOOLBAR_X <= mouse_pos[0] <= TOOLBAR_X + TOOLBAR_WIDTH
                        and TOOLBAR_Y <= mouse_pos[1] <= TOOLBAR_Y + TOOLBAR_HEIGHT
                    ):
                        # Mouse is within toolbar area
                        if mode == "light":
                            if (
                                current_line is None
                            ):  # If no line is currently being drawn
                                current_line = Light(event.pos, event.pos)
                            else:  # If a line is currently being drawn
                                current_line.end = event.pos
                                extended_start, extended_end = (
                                    current_line.calculate_extended_points(screen_size)
                                )
                                extended_line = Light(extended_start, extended_end)
                                lines.append(extended_line)
                                current_line = None
                        elif mode == "mirror":
                            if (
                                current_line is None
                            ):  # If no mirror is currently being drawn
                                current_line = Mirror(event.pos, event.pos)
                            else:  # If a mirror is currently being drawn
                                current_line.update(event.pos)
                                mirrors.append(current_line)
                                current_line = None
                    else:
                        # Mouse is within button area
                        for button in toolbar_buttons:
                            if button.is_clicked():
                                button.click()
            elif event.type == pygame.MOUSEMOTION:
                if (
                    current_line is not None
                ):  # If a line or mirror is currently being drawn
                    current_line.update(event.pos)

        # Fill the win with a color
        win.fill((0, 0, 0))

        # Draw all lines
        for line in lines:
            line.draw(win)

        for line in new_lines:
            line.draw(win)

        if current_line is not None:
            current_line.draw(win)

        # Draw all mirrors
        for mirror in mirrors:
            mirror.draw(win)

        # Draw the toolbar
        pygame.draw.rect(
            win, GRAY, (TOOLBAR_X, TOOLBAR_Y, TOOLBAR_WIDTH, TOOLBAR_HEIGHT)
        )

        # Draw the buttons
        for button in toolbar_buttons:
            button.draw()

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
