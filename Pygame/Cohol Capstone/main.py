import math
import pygame
from settings import Settings

# Program Setup
pygame.init()

# Settings
settings = Settings((1280, 720), (25, 25, 25), 10)

# Screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Circuit Simulator")

# Colors
colors = Settings.get_colors()

# Line Drawing
line_start_pos = None
line_end_pos = None
lines = []
connected_lines = []
click_counter = 0
clock = pygame.time.Clock()
running = True
snap_radius = settings.snap_radius
snap_horizontal = False  # Initialize snap_horizontal
snap_vertical = False  # Initialize snap_vertical


# Util Functions
# Function calculates distances between points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to snap lines to others while in preview mode
def snap_lines(lines, point):
    closest_distance = settings.snap_radius
    closest_end = None
    closest_line_index = None

    for index, line in enumerate(lines):
        for line_end in line:
            dist = distance(point, line_end)
            # Check if the distance is within the snap radius and not directly under the line end
            if dist < closest_distance:
                closest_distance = dist
                closest_end = line_end
                closest_line_index = index

    return closest_end, closest_line_index


def snap_lines_start(lines, point):
    closest_distance = 50
    closest_end = None

    for index, line in enumerate(lines):
        for line_end in line:
            dist = distance(point, line_end)
            # Check if the distance is within the snap radius and not directly under the line end
            if dist < closest_distance:
                closest_end = line_end

    return closest_end


def are_lines_connected(line1, line2):
    # Check if the endpoints of line1 match the endpoints of line2
    if (
        line1[0] == line2[0]
        or line1[0] == line2[1]
        or line1[1] == line2[0]
        or line1[1] == line2[1]
    ):
        return True
    else:
        return False


def save_line(lines: list[tuple[int, int]], coords: tuple[int, int]):
    lines.append([coords[0], coords[1]])


while running:
    # GAME LOGIC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_counter == 0:
                # Check to see if cursor is snapped to line
                closest_end = snap_lines_start(lines, line_end_pos)
                if closest_end is not None:
                    line_start_pos = closest_end
                else:
                    line_start_pos = pygame.mouse.get_pos()
                click_counter += 1
            elif click_counter == 1:
                # Snap the line end to nearby lines if applicable
                closest_end, _ = snap_lines(lines, line_end_pos)
                if closest_end is not None:
                    line_end_pos = closest_end
                    save_line(lines=lines, coords=(line_start_pos, line_end_pos))
                    connected_lines.append((line_start_pos, line_end_pos))
                    click_counter = 0
                else:
                    save_line(lines=lines, coords=(line_start_pos, line_end_pos))
                    click_counter = 0
        elif event.type == pygame.KEYDOWN:
            # Undo Shortcut
            if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                if lines:
                    lines.pop(-1)
            # Vertical and Horizontal snap shortcut
            if event.key == pygame.K_LSHIFT:
                snap_horizontal = True
                snap_vertical = False
            elif event.key == pygame.K_LCTRL:
                snap_horizontal = False
                snap_vertical = True
        elif event.type == pygame.KEYUP:
            # Release the snap
            if event.key == pygame.K_LSHIFT:
                snap_horizontal = False
                snap_vertical = False
            if event.key == pygame.K_LCTRL:
                snap_horizontal = False
                snap_vertical = False

    # RENDER GAME
    screen.fill(settings.screen_color)

    # Menu Bar
    pygame.draw.rect(
        surface=screen,
        color=settings.get_colors()["Gray"],
        rect=pygame.Rect(0, 0, settings.screen_size[0], 60),
    )

    # Line Preview
    if click_counter == 0:
        line_end_pos = pygame.mouse.get_pos()

        # Snap the line end to nearby lines if applicable
        closest_end = snap_lines_start(lines, line_end_pos)

        if closest_end is not None:
            # Draw the circle at the position of closest_end
            pygame.draw.circle(
                surface=screen,
                color=settings.get_colors()["Purple"],
                center=closest_end,  # Draw the circle at the position of closest_end
                radius=10,
            )
        else:
            # Draw the circle at the mouse position when no closest end is found
            pygame.draw.circle(
                surface=screen,
                color=settings.get_colors()["Purple"],
                center=line_end_pos,  # Draw the circle at the current mouse position
                radius=10,
            )

    if click_counter == 1:
        line_end_pos = pygame.mouse.get_pos()

        # Snap the line end to nearby lines if applicable
        closest_end, _ = snap_lines(lines, line_end_pos)
        if closest_end is not None:
            line_end_pos = closest_end

        # Check if Shift key is held down to enforce vertical or horizontal line
        if snap_horizontal:
            line_end_pos = (line_end_pos[0], line_start_pos[1])
        elif snap_vertical:
            line_end_pos = (line_start_pos[0], line_end_pos[1])

        pygame.draw.line(screen, (155, 155, 155), line_start_pos, line_end_pos, 2)

    # Draw Circuits
    for line in lines:
        lines_connected = False
        for other_line in lines:
            if line != other_line and are_lines_connected(line, other_line):
                lines_connected = True
                break
        if lines_connected:
            # Draw the line in a different color to indicate connection
            pygame.draw.line(screen, colors["Green"], line[0], line[1], 3)
        else:
            # Draw the line in the default color
            pygame.draw.line(screen, colors["White"], line[0], line[1], 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
