import numpy as np

PHI = (1 + 5 ** 0.5) / 2

class Polyhedron:
    def __init__(self):
        self.points = []
        self.surfaces = []
        self.connections = []

    def get_points(self):
        return self.points
    
    def get_connections(self):
        return self.connections
    
    def get_surfaces(self):
        return self.surfaces

class Cube(Polyhedron):
    points, connections = [], []

    def __init__(self):
        self.points.append(np.matrix([-1.0, -1.0, 1.0]))
        self.points.append(np.matrix([1.0, -1.0, 1.0]))
        self.points.append(np.matrix([1.0,  1.0, 1.0]))
        self.points.append(np.matrix([-1.0, 1.0, 1.0]))
        self.points.append(np.matrix([-1.0, -1.0, -1.0]))
        self.points.append(np.matrix([1.0, -1.0, -1.0]))
        self.points.append(np.matrix([1.0, 1.0, -1.0]))
        self.points.append(np.matrix([-1.0, 1.0, -1.0]))

        self.surfaces = [
            [0, 1, 2, 3],  # Front
            [5, 4, 7, 6],  # Back
            [4, 0, 3, 7],  # Left
            [1, 5, 6, 2],  # Right
            [1, 0, 4, 5],  # Bottom
            [6, 7, 3, 2]   # Top
        ]

        for p in range(4):
            self.connections.append([p, (p+1) % 4])
            self.connections.append([p+4, ((p+1) % 4) + 4])
            self.connections.append([p, (p+4)])

class Pyramid(Polyhedron):
    points, connections = [], []

    def __init__(self):
        self.points.append(np.matrix([0, -1, 0]))
        self.points.append(np.matrix([-1, 1, 1]))
        self.points.append(np.matrix([1, 1, 1]))
        self.points.append(np.matrix([-1, 1, -1]))
        self.points.append(np.matrix([1, 1, -1]))

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
    points, connections, surfaces = [], [], []

    def __init__(self):
        vertices = [
            [PHI, 1, 0], [PHI, -1, 0], [-PHI, 1, 0], [-PHI, -1, 0],
            [0, PHI, 1], [0, PHI, -1], [0, -PHI, 1], [0, -PHI, -1],
            [1, 0, PHI], [-1, 0, PHI], [1, 0, -PHI], [-1, 0, -PHI]
        ]
        
        for vertex in vertices:
            self.points.append(np.matrix(vertex))

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
