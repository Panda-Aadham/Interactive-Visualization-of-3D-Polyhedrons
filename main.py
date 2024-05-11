import pygame
import numpy as np
from math import *
from shapes import *

# -----------------------------------------
# Contants for the screen and key binds
# -----------------------------------------

# WIDTH, HEIGHT = 1540, 1000
WIDTH, HEIGHT = 800, 600
WHITE = (255,255,255)
CYAN = (0,255,255)
BLACK = (0,0,0)

x_angle, y_angle, z_angle = 0, 0, 0
scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]

pygame.display.set_caption("3D Visualization of Shapes in Python")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

shape = Cube()
points = shape.get_points()
surfaces = shape.get_surfaces()
connections = shape.get_connections()

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0]
])

rotated_points = [
    [n,n,n] for n in range(len(points))
]

projected_points = [
    [n,n] for n in range(len(points))
]

clock = pygame.time.Clock()

# -----------------------------------------
# Main flow of the program
# -----------------------------------------
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scale += 5
            elif event.button == 5:
                scale -= 5

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        y_angle += 0.01
    if keys[pygame.K_LEFT]:
        y_angle -= 0.01
    if keys[pygame.K_UP]:
        x_angle += 0.01
    if keys[pygame.K_DOWN]:
        x_angle -= 0.01
    if keys[pygame.K_LSHIFT]:
        z_angle += 0.01
    if keys[pygame.K_LCTRL]:
        z_angle -= 0.01

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(x_angle), -sin(x_angle)],
        [0, sin(x_angle), cos(x_angle)],
    ])

    rotation_y = np.matrix([
        [cos(y_angle), 0, sin(y_angle)],
        [0, 1, 0],
        [-sin(y_angle), 0, cos(y_angle)],
    ])

    rotation_z = np.matrix([
        [cos(z_angle), -sin(z_angle), 0],
        [sin(z_angle), cos(z_angle), 0],
        [0, 0, 1]
    ])
        
    screen.fill(BLACK)

    # -----------------------------------------
    # Draw each vertex
    # -----------------------------------------
    for index, point in enumerate(points):
        rotated_points[index] = np.dot(rotation_x, point.reshape(3,1))
        rotated_points[index] = np.dot(rotation_y, rotated_points[index])
        rotated_points[index] = np.dot(rotation_z, rotated_points[index])
        projected_2d = np.dot(projection_matrix, rotated_points[index])

        x = int(projected_2d.item(0) * scale) + circle_pos[0]
        y = int(projected_2d[1].item(0) * scale) + circle_pos[1]
        projected_points[index] = [x,y]
        pygame.draw.circle(screen, CYAN, (x,y), 5)
    
    # -----------------------------------------
    # Connect the vertices
    # -----------------------------------------
    for connection in connections:
        first_point = (projected_points[connection[0]][0], projected_points[connection[0]][1])
        second_point = (projected_points[connection[1]][0], projected_points[connection[1]][1])
        pygame.draw.line(screen, WHITE, first_point, second_point)
    
    # -----------------------------------------
    # Draw the surface and its shade
    # -----------------------------------------
    for surf in range(1, len(surfaces) + 1):
        # Get the surface normal
        surface_normal = np.cross(rotated_points[surfaces[surf - 1][1]].flatten() - rotated_points[surfaces[surf - 1][0]].flatten(),
                                  rotated_points[surfaces[surf - 1][2]].flatten() - rotated_points[surfaces[surf - 1][0]].flatten())
        
        # Draw the surface with adjusted color
        if (surface_normal[0][2] > 0):
            light_intensity = 130 + -surface_normal[0][1] * 25
            surface_color = (light_intensity, light_intensity, light_intensity)
            pygame.draw.polygon(screen, surface_color, [projected_points[i] for i in surfaces[surf - 1]])

    pygame.display.update()
