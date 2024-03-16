cube_vertices = [
    # Front
    (-1, 1, 1),
    (-1, -1, 1),
    (-1, -1, -1),
    (-1, 1, -1),
    # Back
    (-3, 1, 1),
    (-3, -1, 1),
    (-3, -1, -1),
    (-3, 1, -1),
]

cube_edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),  # Front face
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),  # Back face
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),  # Connections between front and back faces
]

camera_position = (2, 0, 0)

focal_length = 50

offset = 600


def adjustForCamera(cameraPos, vertices):
    new_vertices = []
    for vertex in vertices:
        x = vertex[0] - cameraPos[0]
        y = vertex[1] - cameraPos[1]
        z = vertex[2] - cameraPos[2]
        print((x, y, z))
        new_vertices.append((x, y, z))
    # print(new_vertices)
    return new_vertices


def calculatePoints(points, focal_length, offset):
    points_array = []
    for point in points:
        x = (focal_length * point[0]) / point[2]
        y = -1 * (focal_length * point[1]) / point[2]
        points_array.append((x + offset // 2, y + offset // 2))
    print(points_array)
    return points_array


calculatePoints(adjustForCamera(camera_position, cube_vertices), focal_length, offset)
