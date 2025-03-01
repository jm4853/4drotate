from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from math import sin, cos
import time

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, axis, theta):
        if axis == 'z':
            t = (
                self.x * cos(theta) - self.y * sin(theta),
                self.x * sin(theta) + self.y * cos(theta),
                self.z,
            )
            self.x = t[0]
            self.y = t[1]
            self.z = t[2]
            return
        if axis == 'y':
            t = (
                self.x * cos(theta) + self.z * sin(theta),
                self.y,
                -1 * self.x * sin(theta) + self.z * cos(theta),
            )
            self.x = t[0]
            self.y = t[1]
            self.z = t[2]
            return
        if axis == 'x':
            t = (
                self.x,
                self.y * cos(theta) - self.z * sin(theta),
                self.y * sin(theta) + self.z * cos(theta),
            )
            self.x = t[0]
            self.y = t[1]
            self.z = t[2]
            return
        print("error")

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class PointSet:
    def __init__(self, points):
        self.points = points

    def rotate(self, axis, theta):
        for p in self.points:
            p.rotate(axis, theta)

    def __str__(self):
        return "[" + ", ".join([str(p) for p in self.points]) + "]"

if __name__ == "__main__":
    # Place points
    s = PointSet([])
    CORNERS = [[1,1,1],[-1,-1,1],[1,-1,-1],[-1,1,-1]]
    for p1 in CORNERS:
        for i in range(3):
            p2 = p1.copy()
            p2[i] *= -1
            s.points.append(PointSet([Point(*p1), Point(*p2)]))

    fig = plt.figure()

    ax = plt.axes(projection='3d')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_aspect('equal')
    
    placed = []
    for l in s.points:
        p1, p2 = l.points
        placed += ax.plot3D([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], 'green')
    plt.pause(0.05)
            
    while True:
        for p in placed:
            p.remove()

        stuff = input("rotation: ")
        if not stuff[0] in ('x', 'y', 'z'):
            print(f"Invalid axis: {stuff[0]}")
            continue
        try:
            theta = float(stuff[1:])
        except:
            print(f"Invalid theta: {stuff[1:]}")
            continue

        s.rotate(stuff[0], theta)

        placed = []
        for l in s.points:
            p1, p2 = l.points
            placed += ax.plot3D([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], 'green')
        
        plt.pause(0.05)
