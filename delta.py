class Delta(object):
    def __init__(self, wx=0, wy=0, wz=0, xy=0, xz=0, yz=0, a=0, b=0, s_h=3):
        self.plane_rotations = {
            'wx': wx,
            'wy': wy,
            'wz': wz,
            'xy': xy,
            'xz': xz,
            'yz': yz,
        }
        self.double_rotation = [a, b]
        self.s_h = s_h # stereo_height
    @property
    def components(self):
        return self.plane_rotations | {'d': self.double_rotation}
    def __getitem__(self, key):
        if key == 'a':
            return self.double_rotation[0]
        if key == 'b':
            return self.double_rotation[1]
        if key == 's':
            return self.s_h
        return self.components[''.join(sorted(key))]
    def __setitem__(self, key, value):
        if key == 'd':
            self.double_rotation = value
        if key == 'a':
            self.double_rotation[0] = value
        if key == 'b':
            self.double_rotation[1] = value
        if key == 's':
            self.s_h = value
        else:
            self.plane_rotations[''.join(sorted(key))] = value
    def items(self): 
        return self.components.items()
    def keys(self):
        return self.components.keys()
    def values(self):
        return self.components.values()
    def __str__(self):
        return str(self.components)


            
