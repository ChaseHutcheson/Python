import pygame
import numpy as np
import math

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.display.set_caption("Perspective Projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

points = [
    # Front Face
    np.matrix([1, 1, 1]),
    np.matrix([1, -1, 1]),
    np.matrix([1, -1, -1]),
    np.matrix([1, 1, -1]),
    # Back Face
    np.matrix([-1, 1, 1]),
    np.matrix([-1, -1, 1]),
    np.matrix([-1, -1, -1]),
    np.matrix([-1, 1, -1]),
]

scale = 100

circle_pos = [WIDTH / 2, HEIGHT / 2]

angle = 0

projection_matrix = np.matrix([[1, 0, 0], [0, 1, 0]])

projected_points = [[n, n] for n in range(len(points))]


def connect_points(i, j, points):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1])
    )


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Updates
    rotation_z = np.matrix(
        [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1],
        ]
    )

    rotation_y = np.matrix(
        [
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)],
        ]
    )

    rotation_x = np.matrix(
        [
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)],
        ]
    )

    angle += 0.01

    screen.fill(WHITE)
    # Draw
    i = 0
    for point in points:
        rotated2D = np.dot(rotation_z, point.reshape(3, 1))
        rotated2D = np.dot(rotation_y, rotated2D)
        rotated2D = np.dot(rotation_x, rotated2D)
        projected2D = np.dot(projection_matrix, rotated2D)
        x = int(projected2D[0][0] * scale) + circle_pos[0]
        y = int(projected2D[1][0] * scale) + circle_pos[1]
        projected_points[i] = [x, y]
        pygame.draw.circle(screen, BLACK, (x, y), 3)
        i += 1

    connect_points(0, 1, projected_points)
    connect_points(1, 2, projected_points)
    connect_points(2, 3, projected_points)
    connect_points(3, 0, projected_points)
    connect_points(4, 5, projected_points)
    connect_points(5, 6, projected_points)
    connect_points(6, 7, projected_points)
    connect_points(7, 4, projected_points)
    connect_points(0, 4, projected_points)
    connect_points(1, 5, projected_points)
    connect_points(2, 6, projected_points)
    connect_points(3, 7, projected_points)

    pygame.display.update()

pygame.quit()
