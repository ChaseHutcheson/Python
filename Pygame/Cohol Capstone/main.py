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

# Toolbar settings
TOOLBAR_WIDTH = WIDTH // 5
TOOLBAR_HEIGHT = HEIGHT
toolbar_rect = pygame.Rect(0, 0, TOOLBAR_WIDTH, TOOLBAR_HEIGHT)

# Drawing settings
drawing = False
mode = "light"

# Button settings
BUTTON_WIDTH = TOOLBAR_WIDTH // 1.2
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10

# Global variables
lines = []
current_line = None

# Font
FONT = pygame.font.Font(None, 32)


# Utils
def intersect(line1, line2):
    x1, y1 = line1.start_pos
    x2, y2 = line1.end_pos if line1.end_pos else line1.extend_to_edge()
    x3, y3 = line2.start_pos
    x4, y4 = line2.end_pos

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Lines are parallel

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    if (
        0 <= t <= 1 and 0 <= u <= 1
    ):  # Ensure intersection point is within both line segments
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1)  # Return intersection point
    else:
        return None


# Classes
class Light:
    def __init__(self, start_pos, screen_size, generation=0):
        self.start_pos = start_pos
        self.end_pos = None
        self.screen_size = screen_size
        self.angle = 0
        self.length = 0
        self.generation = generation
        self.reflected = False

    def draw(self, surface):
        end_pos = self.end_pos if self.end_pos else self.extend_to_edge()
        pygame.draw.line(surface, YELLOW, self.start_pos, end_pos, 2)

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 2 * math.pi  # Ensure angle remains within [0, 2*pi]

    def is_clicked(self, mouse_pos):
        end_pos = self.extend_to_edge()
        distance_to_start = math.dist(self.start_pos, mouse_pos)
        distance_to_end = math.dist(end_pos, mouse_pos)
        return abs(distance_to_start + distance_to_end - self.length) < 5

    def extend_to_edge(self):
        delta_x = math.cos(self.angle)
        delta_y = math.sin(self.angle)
        x = self.start_pos[0]
        y = self.start_pos[1]
        while 0 <= x <= self.screen_size[0] and 0 <= y <= self.screen_size[1]:
            x += delta_x
            y += delta_y
        return (x, y)

    def update_end_pos(self, end_pos, intersection_point=None):
        if intersection_point:
            self.end_pos = intersection_point
            self.reflected = (
                True  # Set reflected to True when the light ray is reflected
            )
        else:
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
        pygame.draw.line(surface, GRAY, self.start_pos, self.end_pos, 10)

    def reflect(self, light, intersection_point):
        # Calculate the angle of incidence
        incidence_angle = self.angle - light.angle

        # The angle of reflection is equal to the angle of incidence
        reflection_angle = self.angle + incidence_angle

        # Create a new light ray that represents the reflected light
        reflected_light = Light(
            intersection_point, light.screen_size, light.generation + 1
        )
        reflected_light.angle = reflection_angle

        return reflected_light


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
        TOOLBAR_WIDTH // 2 - BUTTON_WIDTH // 2,  # Centered horizontally
        TOOLBAR_HEIGHT // 6 * 1 - BUTTON_HEIGHT // 2,  # Evenly spaced vertically
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_BACKGROUND,
        "Light Mode",
        light_button_action,
    ),
    Button(
        TOOLBAR_WIDTH // 2 - BUTTON_WIDTH // 2,  # Centered horizontally
        TOOLBAR_HEIGHT // 6 * 2 - BUTTON_HEIGHT // 2,  # Evenly spaced vertically
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        BUTTON_BACKGROUND,
        "Mirror Mode",
        mirror_button_action,
    ),
]


def main():
    global drawing, current_line, mode
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # New event check
                if event.button == 1:  # 1 is the left mouse button
                    for button in toolbar_buttons:
                        if button.is_clicked():
                            button.click()
                            break
                    else:
                        if mode == "light":
                            current_line = Light(event.pos, (WIDTH, HEIGHT))
                        elif mode == "mirror":
                            current_line = Mirror(event.pos, (WIDTH, HEIGHT))
            elif event.type == pygame.MOUSEMOTION:
                if current_line is not None:
                    dx, dy = (
                        event.pos[0] - current_line.start_pos[0],
                        event.pos[1] - current_line.start_pos[1],
                    )
                    try:
                        current_line.update(event.pos)
                    except:
                        current_line.length = math.hypot(dx, dy)
                        current_line.angle = math.atan2(dy, dx)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if current_line is not None:
                        lines.append(current_line)
                        current_line = None

        # Fill the window
        win.fill(DRAWING_BACKGROUND)

        # Draw the current line
        new_lights = []  # List to hold new light rays
        for line in lines:
            line.draw(win)

            # Check for intersections between light rays and mirrors
            if (
                isinstance(line, Light) and line.generation < 5 and not line.reflected
            ):  # Add the condition here
                closest_intersection = None
                closest_mirror = None
                for mirror in [m for m in lines if isinstance(m, Mirror)]:
                    intersection_point = intersect(line, mirror)
                    if intersection_point is not None:
                        if closest_intersection is None or math.dist(
                            line.start_pos, intersection_point
                        ) < math.dist(line.start_pos, closest_intersection):
                            closest_intersection = intersection_point
                            closest_mirror = mirror
                if closest_intersection is not None:
                    reflected_light = closest_mirror.reflect(line, closest_intersection)
                    new_lights.append(reflected_light)
                    line.update_end_pos(
                        closest_intersection
                    )  # Pass intersection point here

        lines.extend(new_lights)

        # Draw the current line
        if current_line is not None:
            current_line.draw(win)

        # Draw the toolbar
        pygame.draw.rect(win, TOOLBAR_BACKGROUND, toolbar_rect)

        # Draw the buttons
        for button in toolbar_buttons:
            button.draw()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
