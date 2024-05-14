import numpy as np
from math import sqrt

PHI = (1 + 5 ** 0.5) / 2

class Polyhedron:
    points = {}
    surfaces = []
    connections = []

    def get_points(self):
        return self.points.values()
    
    def get_connections(self):
        return self.connections
    
    def get_surfaces(self):
        return self.surfaces
    
    def get_permutations(self, points):
        permutations = []
        # Loop to obtain all permuations
        for i in range(2**3):
            indexes = bin(i)[2:]
            bit_indexes = [i for i, bit in enumerate(indexes[::-1]) if bit == '1']
            permutations.append([point * (-1 if i in bit_indexes else 1) for i, point in enumerate(points)])
        # Return unique lists within the permuatations
        return [list(t) for t in set(tuple(sublist) for sublist in permutations)]


class Cube(Polyhedron):
    def __init__(self):
        self.points[0] = [-1.0, -1.0, 1.0]
        self.points[1] = [1.0, -1.0, 1.0]
        self.points[2] = [1.0,  1.0, 1.0]
        self.points[3] = [-1.0, 1.0, 1.0]
        self.points[4] = [-1.0, -1.0, -1.0]
        self.points[5] = [1.0, -1.0, -1.0]
        self.points[6] = [1.0, 1.0, -1.0]
        self.points[7] = [-1.0, 1.0, -1.0]

        self.surfaces = [
            [1, 5, 6, 2],  # Right
            [4, 0, 3, 7],  # Left
            [6, 7, 3, 2],   # Top
            [1, 0, 4, 5],  # Bottom
            [0, 1, 2, 3],  # Front
            [5, 4, 7, 6],  # Back
        ]

        for p in range(4):
            self.connections.append([p, (p+1) % 4])
            self.connections.append([p+4, ((p+1) % 4) + 4])
            self.connections.append([p, (p+4)])

class Smart_Cube(Polyhedron):
    def __init__(self):
        points = self.get_permutations([1] * 3)
        for index, point in enumerate(points):
            self.points[index] = point
        
        axis_points = [None, None]
        for axis in range(3):
            # Filter the vertices by the current axis
            axis_points[0] = [vertex for vertex in points if vertex[axis] == 1]
            axis_points[1] = [vertex for vertex in points if vertex[axis] == -1]
            for sign in range(2):
                # Get index of the axis to seperate connection pairs
                diff_axis_index = axis + 1 if (axis + 1) < 3 else 0
                sorted_points = sorted(axis_points[sign], key=lambda x: x[diff_axis_index])
                self.connections.append([points.index(sorted_points[0]), points.index(sorted_points[1])])
                self.connections.append([points.index(sorted_points[2]), points.index(sorted_points[3])])
                # Create the surfaces
                surfaces = []
                surface_points = [[1] * 3] if sign == 0 else [[-1] * 3]
                first_axis = (axis + 1 if axis + 1 < 3 else 0) if sign == 0 else (axis - 1 if axis - 1 > -1 else 2)
                second_axis = 3 - (axis + first_axis)
                surfaces.append(points.index(surface_points[0]))
                for i in range(3):
                    surface_points.append(surface_points[i].copy())
                    surface_points[i+1][first_axis if i % 2 == 0 else second_axis] *= -1
                    surfaces.append(points.index(surface_points[i+1]))
                self.surfaces.append(surfaces)

class Pyramid(Polyhedron):
    def __init__(self):
        self.points[0] = [0, -1, 0]
        self.points[1] = [-1, 1, 1]
        self.points[2] = [1, 1, 1]
        self.points[3] = [-1, 1, -1]
        self.points[4] = [1, 1, -1]

        self.surfaces = [
            [2, 1, 0],
            [4, 2, 0],
            [3, 4, 0],
            [1, 3, 0],
            [3, 1, 2, 4],
        ]

        for i in range(1,5):
            self.connections.append([0,i])
        for i in range(1,3):
            self.connections.append([(i*3)-2, 2])
            self.connections.append([(i*3)-2, 3])

class Icosahedron(Polyhedron):
    def __init__(self):
        vertices = [
            [PHI, 1, 0], [PHI, -1, 0], [-PHI, 1, 0], [-PHI, -1, 0],
            [0, PHI, 1], [0, PHI, -1], [0, -PHI, 1], [0, -PHI, -1],
            [1, 0, PHI], [-1, 0, PHI], [1, 0, -PHI], [-1, 0, -PHI]
        ]

        # [PHI, 1, 0], [PHI, -1, 0]
        # [PHI, 1, 0], [0, PHI, 1]
        # [PHI, 1, 0], [0, PHI, -1]
        # [PHI, 1, 0], [1, 0, PHI]
        # [PHI, 1, 0], [1, 0, -PHI]
        
        for index, vertex in enumerate(vertices):
            self.points[index] = vertex

        # Compute the connections
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                distance = np.linalg.norm(np.array(vertices[i]) - np.array(vertices[j]))
                if abs(distance) == 2.0:
                    self.connections.append([i, j])

        self.generate_surfaces()
    
    def generate_surfaces(self):
        # Define the indices of vertices forming each triangle surface
        self.surfaces = [
            [0, 1, 4], [0, 4, 8], [0, 8, 9], [0, 9, 2], [0, 2, 1],
            [3, 2, 9], [3, 9, 11], [3, 11, 7], [3, 7, 5], [3, 5, 2],
            [6, 1, 2], [6, 2, 5], [6, 5, 10], [6, 10, 4], [6, 4, 1],
            [7, 8, 4], [7, 4, 10], [7, 10, 11], [7, 11, 9], [7, 9, 8],
            [10, 5, 7], [10, 7, 11], [10, 11, 9], [10, 9, 8], [10, 8, 4]
        ]
        return self.surfaces

class Smart_Icosahedron(Polyhedron):
    def __init__(self):
        for i in range(3):
            points = [0] * 3
            points[i] = PHI
            points[0 if i==2 else i+1] = 1
            all_points = self.get_permutations(points)
            for index, point in enumerate(all_points):
                self.points[index + (i * len(all_points))] = point

        # Use euclidean distance formula to get connections
        points = self.points
        for x in range(len(points)):
            for y in range(x + 1, len(points)):
                distance_sq = [(points[x][i] - points[y][i]) ** 2 for i in range(len(points[x]))]
                distance = sqrt(sum(distance_sq))
                if distance == 2:
                    self.connections.append([x,y])

        self.find_min_sides()

    def find_min_sides(self):
        vertex_to_find, distances = 0, []
        paths_taken = [self.connections[0]]
        current_vertex = paths_taken[0][1]
        distances.append(self.dfs(vertex_to_find, current_vertex, paths_taken, 1))
        print(distances)
        
        # for edge in edges:
        #     if edge not in paths_taken:
        #         current_vertex = edge[0 if edges[0] != current_vertex else 1]
        #         paths_taken.append(edge)
        #         break

    def dfs(self, find, current_vertex, paths_taken, steps):
        edges = [edge for edge in self.connections if current_vertex in edge]
        distances = []
        print(edges)
        for edge in edges:
            print("pt", paths_taken)
            if edge not in paths_taken:
                if find in edge:
                    return steps + 1
                else:
                    current_vertex = edge[0 if current_vertex != edge[0] else 1]
                    distances.append(self.dfs(find, current_vertex, paths_taken + [edge], steps + 1))
        return distances