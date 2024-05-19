import pygame
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

shape = Smart_Icosahedron()
points = shape.get_points()
surfaces = shape.get_surfaces()
connections = shape.get_connections()

projection_matrix = [[1,0,0],
                     [0,1,0],
                     [0,0,0]]

rotated_points = [
    [n,n,n] for n in range(len(points))
]

projected_points = [
    [n,n] for n in range(len(points))
]

def dot_product(vector,matrix):
    return [sum(vector[j] * matrix[i][j] for j in range(len(vector))) for i in range(len(matrix))]

# -----------------------------------------
# Shape controller function
# -----------------------------------------
def shape_controller(keys, x_angle, y_angle, z_angle):
    # Rotating
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

    # Positioning
    if keys[pygame.K_a]:
        for point in points:
            point[0] -= 0.05
    if keys[pygame.K_d]:
        for point in points:
            point[0] += 0.05
    if keys[pygame.K_s]:
        for point in points:
            point[1] -= 0.05
    if keys[pygame.K_w]:
        for point in points:
            point[1] += 0.05
    if keys[pygame.K_q]:
        for point in points:
            point[2] -= 0.05
    if keys[pygame.K_e]:
        for point in points:
            point[2] += 0.05
    
    return x_angle, y_angle, z_angle

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
    if True in keys:
        x_angle, y_angle, z_angle = shape_controller(keys, x_angle, y_angle, z_angle)

    # Rotation matrices
    rotation_x = [[1, 0, 0],
                  [0, cos(x_angle), -sin(x_angle)],
                  [0, sin(x_angle), cos(x_angle)]]

    rotation_y = [[cos(y_angle), 0, sin(y_angle)],
                  [0, 1, 0],
                  [-sin(y_angle), 0, cos(y_angle)]]

    rotation_z = [[cos(z_angle), -sin(z_angle), 0],
                  [sin(z_angle), cos(z_angle), 0],
                  [0, 0, 1]]
        
    screen.fill(BLACK)

    # -----------------------------------------
    # Draw each vertex
    # -----------------------------------------
    for index, point in enumerate(points):
        rotated_points[index] = dot_product(point, rotation_x)
        rotated_points[index] = dot_product(rotated_points[index], rotation_y)
        rotated_points[index] = dot_product(rotated_points[index], rotation_z)
        projected_2d = dot_product(rotated_points[index], projection_matrix)

        x = int(projected_2d[0] * scale) + circle_pos[0]
        y = int(projected_2d[1] * scale) + circle_pos[1]
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
    for surface in range(len(surfaces)):
        # Calculate the two vectors to use in cross product
        vector1, vector2 = [0]*3, [0]*3
        for index in range(3):
            vector1[index] = rotated_points[surfaces[surface][1]][index] - rotated_points[surfaces[surface][0]][index]
            vector2[index] = rotated_points[surfaces[surface][2]][index] - rotated_points[surfaces[surface][0]][index]
        
        # Calculate surface normal using cross product:
        # x = v1[1] * v2[2] - v1[2] * v2[1]
        # y = v1[2] * v2[0] - v1[0] * v2[2]
        # z = v1[0] * v2[1] - v1[1] * v2[0]
        surface_normal = []
        for axis in range(3):
            first = axis + 1 if axis + 1 < 3 else 0
            second = first + 1 if first + 1 < 3 else 0
            surface_normal.append((vector1[first] * vector2[second]) - (vector1[second] * vector2[first]))
        
        # Draw the surface with adjusted color
        if (surface_normal[2] > 0):
            light_intensity = 130 + -surface_normal[1] * 25
            surface_color = (light_intensity, light_intensity, light_intensity)
            # pygame.draw.polygon(screen, surface_color, [projected_points[i] for i in surfaces[surface]])

    pygame.display.update()
