import math


# Function calculates distances between points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point2[1] - point2[1]) ** 2)


# Function to snap lines to others while in preview mode
def snapLines(lines, point):
    closest_distance = 10
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
