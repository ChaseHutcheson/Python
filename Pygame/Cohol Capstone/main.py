import pygame
import math
import pygame_gui

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Line Creator with GUI")

# Create a clock
clock = pygame.time.Clock()

# Create a manager for GUI elements
manager = pygame_gui.UIManager((1280, 720))

# Create buttons for toggling line mode and button mode
toggle_line_mode_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (100, 50)),  # Position and size
    text='Line Mode: OFF',
    manager=manager
)

toggle_button_mode_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 10), (100, 50)),  # Position and size
    text='Button Mode: OFF',
    manager=manager
)

# Variables for tracking line mode, button mode, and mouse clicks
line_mode = False
button_mode = False
click_counter = 0
start_pos = None
lines = []  # List of tuples (start_pos, end_pos)
connected_lines = []  # List of arrays storing connected lines indices
buttons = []  # List of button objects
snap_radius = 10  # Define a radius around line ends for snapping

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point2[1] - point2[1]) ** 2)

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

# Function to find the closest point on a line segment to a given point
def find_closest_point_on_line_segment(line, point):
    # Unpack the line points
    start, end = line
    # Calculate the line vector
    line_vector = (end[0] - start[0], end[1] - start[1])
    # Calculate the length squared of the line vector
    length_squared = line_vector[0] ** 2 + line_vector[1] ** 2
    
    # If the line is just a point
    if length_squared == 0:
        return start

    # Calculate the projection of the point onto the line
    t = ((point[0] - start[0]) * line_vector[0] + (point[1] - start[1]) * line_vector[1]) / length_squared
    
    # Clamp t between 0 and 1 to keep the point on the line segment
    t = max(0, min(1, t))
    
    # Calculate the closest point on the line segment
    closest_point = (
        start[0] + t * line_vector[0],
        start[1] + t * line_vector[1]
    )
    
    return closest_point

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

# Class for button objects
class Button:
    def __init__(self, position, line_index):
        self.position = position
        self.line_index = line_index
        self.state = False  # Initial state is off
    
    def toggle(self):
        self.state = not self.state
    
    def draw(self, screen):
        # Set color based on state
        color = YELLOW if self.state else PURPLE
        pygame.draw.circle(screen, color, self.position, 8)  # Draw button as a circle

# Function to power lines based on a button's state
def power_lines(start_line_index, powered_lines):
    if start_line_index not in powered_lines:
        powered_lines.append(start_line_index)
        
        # Recursively power lines connected to the start line
        for conn_line in connected_lines:
            if conn_line[0] == start_line_index and conn_line[1] not in powered_lines:
                power_lines(conn_line[1], powered_lines)
            elif conn_line[1] == start_line_index and conn_line[0] not in powered_lines:
                power_lines(conn_line[0], powered_lines)

# Main loop
running = True
# Rest of the script remains the same

# In the main loop:

while running:
    # Process events
    for event in pygame.event.get():
        # Handle quitting
        if event.type == pygame.QUIT:
            running = False
        
        # Add this line to capture the state of the keys
        keys = pygame.key.get_pressed()
        
        # Handle mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Your existing code here...

            # Check if the click is within the bounds of the buttons
            click_pos = pygame.mouse.get_pos()
            line_mode_button_rect = toggle_line_mode_button.rect
            button_mode_button_rect = toggle_button_mode_button.rect
            
            click_within_line_button = line_mode_button_rect.collidepoint(click_pos)
            click_within_button_mode_button = button_mode_button_rect.collidepoint(click_pos)
            
            # If button mode is enabled and the click is outside the buttons
            if button_mode and not (click_within_line_button or click_within_button_mode_button):
                # Find the closest point on a line to the mouse click position
                closest_point, line_index = find_closest_line_end(click_pos)
                
                if closest_point is not None:
                    # Create a new button at the closest point on the line
                    new_button = Button(closest_point, line_index)
                    buttons.append(new_button)
            
            # If line mode is enabled and the click is outside the buttons
            if line_mode and not (click_within_line_button or click_within_button_mode_button):
                if click_counter == 0:
                    # Store the start position of the line
                    start_pos = click_pos
                    click_counter += 1
                elif click_counter == 1:
                    # Check if the Shift key is being held down
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        # Snap the end position to the closest horizontal or vertical angle
                        end_pos = snap_rotation(start_pos, click_pos)
                    else:
                        # If not holding Shift, use the mouse position directly
                        end_pos = click_pos
                    
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
        
        # Handle button clicks
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == toggle_line_mode_button:
                # Toggle line mode
                line_mode = not line_mode
                # Update the button text based on the line mode state
                toggle_line_mode_button.set_text(f"Line Mode: {'ON' if line_mode else 'OFF'}")
                # Disable button mode when line mode is enabled
                if line_mode:
                    button_mode = False
                    toggle_button_mode_button.set_text("Button Mode: OFF")
            elif event.ui_element == toggle_button_mode_button:
                # Toggle button mode
                button_mode = not button_mode
                # Update the button text based on the button mode state
                toggle_button_mode_button.set_text(f"Button Mode: {'ON' if button_mode else 'OFF'}")
                # Disable line mode when button mode is enabled
                if button_mode:
                    line_mode = False
                    toggle_line_mode_button.set_text("Line Mode: OFF")
            
            # If a button is clicked in button mode
            if button_mode and event.type == pygame.MOUSEBUTTONDOWN:
                # Find the closest point on a line to the mouse click position
                closest_point, line_index = find_closest_point_on_line_segment(lines[0], pygame.mouse.get_pos())
                
                if closest_point is not None:
                    # Create a new button at the closest point on the line
                    button = Button(closest_point, line_index)
                    buttons.append(button)
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Draw all the lines stored in the list
    for line in lines:
        pygame.draw.line(screen, WHITE, line[0], line[1], 2)
    
    # Draw buttons on lines and power connected lines if button state is ON
    for button in buttons:
        button.draw(screen)
        if button.state:
            powered_lines = []
            power_lines(button.line_index, powered_lines)
            for index in powered_lines:
                pygame.draw.line(screen, YELLOW, lines[index][0], lines[index][1], 2)
    
    # Draw purple circles at the ends of lines to provide snapping points
    for line in lines:
        pygame.draw.circle(screen, PURPLE, line[0], snap_radius)
        pygame.draw.circle(screen, PURPLE, line[1], snap_radius)
    
    # Draw a button preview if in button mode
    if button_mode:
        # Find the closest point on a line to the mouse position
        cursor_pos = pygame.mouse.get_pos()
        closest_point, _ = find_closest_line_end(cursor_pos)
        
        # Only draw if the closest point is not None
        if closest_point:
            # Draw the button preview as a red circle with text indicating state
            pygame.draw.circle(screen, RED, closest_point, 8)
            font = pygame.font.Font(None, 20)
            text = font.render("On" if buttons and buttons[-1].state else "Off", True, WHITE)
            screen.blit(text, (closest_point[0] + 10, closest_point[1]))
    
    # Draw line mode preview if in line mode
    if line_mode and start_pos is not None:
        # Draw the line from the start position to the mouse position
        end_pos = pygame.mouse.get_pos()
        
        # Check if snapping is required
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            # Snap the end position to the closest horizontal or vertical angle
            end_pos = snap_rotation(start_pos, end_pos)
        
        # Draw the line preview
        pygame.draw.line(screen, PURPLE, start_pos, end_pos, 2)
    
    # Update the GUI
    manager.update(pygame.time.get_ticks())
    manager.draw_ui(screen)
    
    # Update the display
    pygame.display.update()
    
    # Cap the frame rate to 60 frames per second
    clock.tick(60)

pygame.quit()

