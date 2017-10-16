import ratcave as rc
import numpy as np
import pyglet

obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)

class Geometry(object):

    def __init__(self, mesh, x, y, color, speed=10., scale=0.5):
        pass

        self.mesh = obj_reader.get_mesh(mesh, position=(0, 0, -7), scale=scale)
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


class Bat(Geometry):
    def __init__(self, x, y, color):
        super().__init__(mesh='Cube', x=x, y=y, color=color, scale=0.5)


class Ball(Geometry):

    def __init__(self, x, y, color, speed=1., angle=170):
        super().__init__(mesh='Sphere', x=x, y=y, color=color, scale=0.2)
        self.speed = speed
        self.angle = angle
        # self.sound = pyglet.media.load('PPB.wav', streaming=False)
        pyglet.clock.schedule(self.update)

    def update(self, dt):
        self.x += self.speed * np.cos(np.degrees(self.angle)) * dt
        self.y += self.speed * np.sin(np.degrees(self.angle)) * dt

    def bounce(self, bounce_dir):
        if bounce_dir:
            self.angle = 180 - self.angle
            print('Bounced left/right!!')
        else:
            self.angle = 180 - self.angle
            print('Bounced up/down!!')

        # self.sound.play()

