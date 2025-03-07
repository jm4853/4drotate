from delta import Delta
from draw import Drawer, Drawer2D
from points import PointServer
# from shell import Shell
import time

if __name__ == '__main__':
    delta = Delta(a=0.05559016, b=0.005)
    # draw = Drawer()
    drawer = Drawer2D()
    line_server = PointServer(delta, mode='2d')
    # shell = Shell(delta)

    for lines in line_server:
        drawer.draw(lines)
