from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from threading import Thread
from math import sin, cos
import time

# matplotlib.use('qt6agg')
plt.ion()

class Point:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def rotate(self, axis, theta):
        loop = True
        while loop:
            # https://math.stackexchange.com/questions/1402362/can-rotations-in-4d-be-given-an-explicit-matrix-form
            if axis == 'xy':
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.y * sin(theta),
                    self.x * sin(theta) + self.y * cos(theta),
                    self.z,
                    self.w,
                )
                return
            if axis == 'xz':
                self.x, self.y, self.z, self.w = (
                    self.x,
                    self.y * cos(theta) - self.w * sin(theta),
                    self.z,
                    self.y * sin(theta) + self.w * cos(theta),
                )
                return
            if axis == 'xw':
                self.x, self.y, self.z, self.w = (
                    self.x,
                    self.y * cos(theta) - self.z * sin(theta),
                    self.y * sin(theta) + self.z * cos(theta),
                    self.w,
                )
                return
            if axis == 'yz':
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.w * sin(theta),
                    self.y,
                    self.z,
                    self.x * sin(theta) + self.w * cos(theta),
                )
                return
            if axis == 'yw':
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.z * sin(theta),
                    self.y,
                    self.x * sin(theta) + self.z * cos(theta),
                    self.w,
                )
                return
            if axis == 'zw':
                self.x, self.y, self.z, self.w = (
                    self.x,
                    self.y,
                    self.z * cos(theta) - self.w * sin(theta),
                    self.z * sin(theta) + self.w * cos(theta),
                )
                return
            axis = axis[1] + axis[0]
            loop = False
        print("error")
        return 1

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

delta = None


def deltaThread():
    global delta
    def parseMag(mag, axis):
        s = 1
        if mag[0] == '-':
            s = -1
            mag = mag.replace('-', '+')
        if mag[0] == '+':
            t = mag[:mag.rfind('+') + 1]
            if set(t) != {'+'}:
                print(f"Invalid magnitude")
                return delta[axis]
            exp = len(t)
            t = mag[mag.rfind('+') + 1:]
            try:
                t = float(t)
            except:
                t = 1
            return delta[axis] + s * t * (10 ** (-1 * (6 - exp)))
        else:
            try:
                return float(mag)
            except:
                print(f"Invalid magnitude: {mag}")
            return delta[axis]
    
    delta_cache = None
    while True:
        print(f"{'\n'.join([f'{k} {v}' for k, v in (delta_cache if delta_cache else delta).items() if v])}")
        line = input(f"{'*' if delta_cache else ' '}> ")
        if not line:
            continue
        if line[0] == 'p':
            if delta_cache:
                delta = delta_cache
                delta_cache = None
            else:
                delta_cache = delta.copy()
                delta = {k: 0 for k, _ in delta.items()}
            continue
        if len(line.split()) != 2:
            print(f"Invalid rotation, expected: \"[plane] [magnitude]\"")
            continue
        axis, mag = line.split()
        axis = axis.lower()

        if not axis in delta.keys():
            if not axis[1] + axis[0] in delta.keys():
                print(f"Invalid plane: {axis}")
                continue
            axis = axis[1] + axis[0]

        # delta[axis] = parseMag(mag, axis)
        delta[axis] = float(mag)



if __name__ == "__main__":
    # Place points
    s = PointSet([])
    # CORNERS = [[1,1,1],[-1,-1,1],[1,-1,-1],[-1,1,-1]]
    CORNERS = [[1,1,1,1],[-1,-1,1,1],[1,-1,-1,1],[-1,1,-1,1],[-1,-1,-1,-1],[1,1,-1,-1],[-1,1,1,-1],[1,-1,1,-1]]
    for p1 in CORNERS:
        for i in range(4):
            p2 = p1.copy()
            p2[i] *= -1
            s.points.append(PointSet([Point(*p1), Point(*p2)]))

    fig = plt.figure()

    ax = plt.axes(projection='3d')

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.set_aspect('equal')
    
    placed = []
    for l in s.points:
        p1, p2 = l.points
        placed += ax.plot3D([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], 'green')
        # placed += ax.plot3D(p1.x, p1.y, p1.z, 'bo')
        # placed += ax.plot3D(p2.x, p2.y, p2.z, 'bo')
    plt.pause(0.05)
    delta = {
        'zw': -0.05,
        'yw': 0,
        'yz': 0,
        'xw': 0,
        'xz': 0,
        'xy': 0.03125,
    }
    s.rotate('xw', 1)
    s.rotate('xy', 5)

    thread = Thread(target = deltaThread)
    thread.start()
            
    while True:
        for p in placed:
            p.remove()

        for a, mag in delta.items():
            s.rotate(a, mag)
        # # 0.08381
        # s.rotate('xy', -0.05)
        # s.rotate('zw', 0.03125)
        # s.rotate('xw', 0.04797)
        # s.rotate('xw', -0.01307)

        placed = []
        for l in s.points:
            p1, p2 = l.points
            placed += ax.plot3D([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], 'green')
            # placed += ax.plot3D(p1.x, p1.y, p1.z, 'bo')
            # placed += ax.plot3D(p2.x, p2.y, p2.z, 'bo')
        
        plt.pause(0.01)
