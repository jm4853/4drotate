import matplotlib.pyplot as plt
import copy

plt.ion()

class Drawer:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_zlim(-3, 3)
        self.ax.set_aspect('equal')
        self.placed = []


    def draw(self, lines):
        for p in self.placed:
            p.remove()
        self.placed = []

        for (x1, y1, z1), (x2, y2, z2) in lines:
            self.placed += self.ax.plot3D([x1, x2], [y1, y2], [z1, z2], 'green')
            self.placed += self.ax.plot3D(x1, y1, z1, 'bo')
            self.placed += self.ax.plot3D(x2, y2, z2, 'bo')
        plt.pause(0.01)

class Drawer2D:
    def __init__(self):
        self.fig = plt.figure()
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.axis('scaled')
        self.placed = []


    def draw(self, lines):
        for p in self.placed:
            p.remove()
        self.placed = []

        for (x1, y1), (x2, y2) in lines:
            self.placed += plt.plot([x1, x2], [y1, y2], 'green')
            self.placed += plt.plot(x1, y1, 'bo')
            self.placed += plt.plot(x2, y2, 'bo')
        plt.pause(0.01)
