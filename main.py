from delta import Delta
from draw import Drawer, Drawer2D
from points import PointServer, CPointServer
# from shell import Shell
import time

if __name__ == '__main__':
    delta = Delta(a=0.005, b=0.05559016, h=2.3)
    drawer = Drawer()
    line_server = CPointServer(delta)
    # shell = Shell(delta)

    for lines in line_server:
        drawer.draw(lines)

