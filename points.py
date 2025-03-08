from math import sin, cos
import ctypes as ct

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
        axis = set(axis)
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
        print("error")
        return 1
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

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

def makeLines():
    s = PointSet([])
    CORNERS = [[1,1,1,1],[-1,-1,1,1],[1,-1,-1,1],[-1,1,-1,1],[-1,-1,-1,-1],[1,1,-1,-1],[-1,1,1,-1],[1,-1,1,-1]]
    for p1 in CORNERS:
        for i in range(4):
            p2 = p1.copy()
            p2[i] *= -1
            s.points.append(PointSet([Point(*p1), Point(*p2)]))
    return s
    
class PointServer:
    def __init__(self, delta, lines=None, mode='3d'):
        self.delta = delta
        self.lines = lines if lines else makeLines()
        self.mode = mode

    def _projection2d(self, x, y, z):
        x, z = z, x
        return (
            x / (1.9 - z),
            y / (1.9 - z),
        )
    def _projection(self, p):
        x, y, z, w = p.tuple()
        t = (
            x / (self.delta.h - w),
            y / (self.delta.h - w),
            z / (self.delta.h - w),
        )
        if self.mode == '2d':
            return self._projection2d(*t)
        return t

    def __iter__(self):
        return self

    def __next__(self):
        for axis, mag in self.delta.items():
            self.lines.rotate(axis, mag)
        return [
            (self._projection(p1), self._projection(p2))
            for p1, p2 in [l.points for l in self.lines.points]
        ]

class CPointServer:
    def __init__(self, delta, lines=None):
        self.delta = delta
        self.lines = None
        self.funcs = ct.CDLL('./lib/rotate.so')
        self.funcs.init_lines()
        self.funcs.get.restype = ct.c_double
    def __iter__(self):
        return self
    def __next__(self):
        self.funcs.do_rotation(ct.c_double(self.delta['a']), ct.c_double(self.delta['b']), ct.c_double(self.delta.h))
        return [[[self.funcs.get(ct.c_int(i), ct.c_int(j), ct.c_int(k)) for k in range(3)] for j in range(2)] for i in range(32)]

