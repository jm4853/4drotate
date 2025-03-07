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

    def tuple(self):
        return self.x, self.y, self.z, self.w

    def double_rotate(self, alpha, beta):
        self.x, self.y, self.z, self.w = (
            self.x * cos(alpha) - self.y * sin(alpha),
            self.x * sin(alpha) + self.y * cos(alpha),
            self.z * cos(beta) - self.w * sin(beta),
            self.z * sin(beta) + self.w * cos(beta),
        )


    def rotate(self, axis, theta):
        loop = True
        axis = set(axis)
        while loop:
            # https://math.stackexchange.com/questions/1402362/can-rotations-in-4d-be-given-an-explicit-matrix-form
            if axis == {'x', 'y'}:
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.y * sin(theta),
                    self.x * sin(theta) + self.y * cos(theta),
                    self.z,
                    self.w,
                )
                return
            if axis == {'x', 'z'}:
                self.x, self.y, self.z, self.w = (
                    self.x,
                    self.y * cos(theta) - self.w * sin(theta),
                    self.z,
                    self.y * sin(theta) + self.w * cos(theta),
                )
                return
            if axis == {'x', 'w'}:
                self.x, self.y, self.z, self.w = (
                    self.x,
                    self.y * cos(theta) - self.z * sin(theta),
                    self.y * sin(theta) + self.z * cos(theta),
                    self.w,
                )
                return
            if axis == {'y', 'z'}:
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.w * sin(theta),
                    self.y,
                    self.z,
                    self.x * sin(theta) + self.w * cos(theta),
                )
                return
            if axis == {'y', 'w'}:
                self.x, self.y, self.z, self.w = (
                    self.x * cos(theta) - self.z * sin(theta),
                    self.y,
                    self.x * sin(theta) + self.z * cos(theta),
                    self.w,
                )
                return
            if axis == {'z', 'w'}:
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

    def tuple(self):
        return [p.tuple() for p in self.points]

    def double_rotate(self, alpha, beta):
        for p in self.points:
            p.double_rotate(alpha, beta)

    def _rotate(self, axis, theta):
        for p in self.points:
            p.rotate(axis, theta)

    def rotate(self, *args):
        if args[0][0] == 'd':
            return self.double_rotate(*args[1])
        return self._rotate(*args)

    def __str__(self):
        return "[" + ", ".join([str(p) for p in self.points]) + "]"

def doStereography(point):
    x, y, z, w = point
    return (
        x / (HEIGHT - w),
        y / (HEIGHT - w),
        z / (HEIGHT - w),
        w / (HEIGHT - w),
    )

def doNone(*args):
    return args[0]

delta = None
PROJECTION = doNone
HEIGHT = 3

        

def deltaThread():
    global delta, PROJECTION, HEIGHT
    
    delta_cache = None
    while True:
        print(f"{'\n'.join([f'{k} {v}' for k, v in (delta_cache if delta_cache else delta).items() if v])}")
        line = input(f"{'*' if delta_cache else ' '}> ")
        if not line:
            continue
        if line[0] == 'z':
            delta = {k: 0 for k, _ in delta.items()}
            continue
        if line[0] == 'p':
            if delta_cache:
                delta = delta_cache
                delta_cache = None
            else:
                delta_cache = delta.copy()
                delta = {k: 0 for k, _ in delta.items()}
            continue
        if line[0] == 'd':
            try:
                delta['d'] = [float(line.split()[1]), float(line.split()[2])]
            except:
                print(f"Invalid double angle parameters: {line}")
            continue
        if line[0] == 's':
            try:
                if len(line.split()) == 1:
                    PROJECTION = doNone
                else:
                    HEIGHT = float(line.split()[1])
                    PROJECTION = doStereography
            except Exception as e:
                print(f"Bad line: {line}")
                print(f"{e}")
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
        x1, y1, z1, w1, = PROJECTION(p1.tuple())
        x2, y2, z2, w2, = PROJECTION(p2.tuple())
        
        placed += ax.plot3D([x1, x2], [y1, y2], [z1, z2], 'green')
        placed += ax.plot3D(x1, y1, z1, 'bo')
        placed += ax.plot3D(x2, y2, z2, 'bo')
    plt.pause(0.05)
    # delta = {
    #     'zw': -0.05,
    #     'yw': 0,
    #     'yz': 0,
    #     'xw': 0,
    #     'xz': 0,
    #     'xy': 0.03125,
    # }
    # s.rotate('xw', 1)
    # s.rotate('xy', 5)
    delta = {
        'zw': 0,
        'yw': 0,
        'yz': 0,
        'xw': 0,
        'xz': 0,
        'xy': 0,
    }

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
            x1, y1, z1, w1, = PROJECTION(p1.tuple())
            x2, y2, z2, w2, = PROJECTION(p2.tuple())
            # x1, y1, z1, w1, = doStereography(p1.tuple())
            # x2, y2, z2, w2, = doStereography(p2.tuple())
            
            placed += ax.plot3D([x1, x2], [y1, y2], [z1, z2], 'green')
            placed += ax.plot3D(x1, y1, z1, 'bo')
            placed += ax.plot3D(x2, y2, z2, 'bo')
        
        plt.pause(0.01)
