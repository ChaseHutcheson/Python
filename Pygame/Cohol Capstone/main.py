import pygame
import math
import pygame_gui  # Import pygame_gui

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Line Creator with GUI")

# Create a clock
clock = pygame.time.Clock()

# Create a manager for GUI elements
manager = pygame_gui.UIManager((1280, 720))

# Create a button for toggling line mode
toggle_line_mode_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (100, 50)),  # Position and size
    text='Line Mode: OFF',
    manager=manager
)

# Variables for tracking line mode and mouse clicks
line_mode = False
click_counter = 0
start_pos = None
lines = []  # List of tuples (start_pos, end_pos)
connected_lines = []  # List of arrays storing connected lines indices
snap_radius = 10  # Define a radius around line ends for snapping

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Function to find the closest line end to a point within the snap radius
def find_closest_line_end(point):
    closest_distance = snap_radius
    closest_end = None
    closest_line_index = None

    for index, line in enumerate(lines):
        # Check the distance to both the start and end points of each line
        for line_end in line:
            dist = distance(point, line_end)
            if dist < closest_distance:
                closest_distance = dist
                closest_end = line_end
                closest_line_index = index
    
    return closest_end, closest_line_index

# Function to snap the rotation of the line based on the shift key
def snap_rotation(start_pos, cursor_pos):
    dx = cursor_pos[0] - start_pos[0]
    dy = cursor_pos[1] - start_pos[1]
    
    # Calculate the angle in radians
    angle = math.atan2(dy, dx)
    
    # Snap to the closest horizontal or vertical angle
    if -math.pi/4 <= angle < math.pi/4:
        # 0° (horizontal line)
        end_pos = (start_pos[0] + dx, start_pos[1])
    elif math.pi/4 <= angle < 3 * math.pi/4:
        # 90° (vertical line)
        end_pos = (start_pos[0], start_pos[1] + dy)
    elif -3 * math.pi/4 <= angle < -math.pi/4:
        # -90° (vertical line)
        end_pos = (start_pos[0], start_pos[1] + dy)
    else:
        # 180° (horizontal line)
        end_pos = (start_pos[0] + dx, start_pos[1])
    
    return end_pos

# Main loop
running = True
while running:
    # Get current state of keyboard
    keys = pygame.key.get_pressed()
    
    # Process events
    for event in pygame.event.get():
        # Handle quitting
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if line_mode:
                if click_counter == 0:
                    # Store the start position of the line
                    start_pos = event.pos
                    click_counter += 1
                elif click_counter == 1:
                    # Check if the Shift key is being held down
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        # Snap the end position to the closest horizontal or vertical angle
                        end_pos = snap_rotation(start_pos, event.pos)
                    else:
                        # If not holding Shift, use the mouse position directly
                        end_pos = event.pos
                    
                    # Check if the end position is close to any line end for snapping
                    snapped_end, connected_line_index = find_closest_line_end(end_pos)
                    if snapped_end:
                        # If the mouse end of the line is snapped, use the snapped position
                        end_pos = snapped_end
                        # Store the indices of the connected lines
                        connected_lines.append([len(lines), connected_line_index])
                    
                    # Store the new line in the list
                    lines.append((start_pos, end_pos))
                    # Reset click counter
                    click_counter = 0
        
        # Handle GUI events
        manager.process_events(event)
        
        # Handle button click
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == toggle_line_mode_button:
                # Toggle line mode
                line_mode = not line_mode
                # Update the button text based on the line mode state
                if line_mode:
                    toggle_line_mode_button.set_text("Line Mode: ON")
                else:
                    toggle_line_mode_button.set_text("Line Mode: OFF")
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Draw all the lines stored in the list
    for line in lines:
        pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 2)
    
    # Draw purple circles at the ends of the lines to provide snapping points
    for line in lines:
        pygame.draw.circle(screen, (128, 0, 128), line[0], snap_radius)  # Draw circle at start of line
        pygame.draw.circle(screen, (128, 0, 128), line[1], snap_radius)  # Draw circle at end of line
    
    # If in preview mode, draw a line from the start position to the current cursor position
    if line_mode and click_counter == 1:
        # Get the current cursor position
        cursor_pos = pygame.mouse.get_pos()
        
        # Check if the Shift key is being held down
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            # Snap the rotation of the line to the closest horizontal or vertical angle
            cursor_pos = snap_rotation(start_pos, cursor_pos)
        
        # Check if the cursor end of the line is close to any line end for snapping
        snapped_end, _ = find_closest_line_end(cursor_pos)
        if snapped_end:
            # Use the snapped end position if within the threshold
            cursor_pos = snapped_end
        
        # Draw the preview line
        pygame.draw.line(screen, (255, 255, 255), start_pos, cursor_pos, 1)
    
    # Update the GUI
    manager.update(pygame.time.get_ticks())
    manager.draw_ui(screen)
    
    # Update the display
    pygame.display.update()
    
    # Cap the frame rate to 60 frames per second
    clock.tick(60)

pygame.quit()
