import ratcave as rc

obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)

class Bat(object):

    def __init__(self, x, y, color, speed=10., *args, **kwargs):
        pass

        self.mesh = obj_reader.get_mesh('Cube', position=(0, 0, -7), scale=.5)
        self.mesh.uniforms['diffuse'] = color
        self.x = x
        self.y = y
        self.speed = speed


    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.mesh.position.x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value
        self.mesh.position.y = value

    @property
    def xyz(self):
        return tuple(self.mesh.position.xyz)