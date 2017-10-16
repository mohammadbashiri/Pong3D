import ratcave as rc
import numpy as np
import pyglet

obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)

class Ball(object):

    def __init__(self, x, y, color, speed=1., angle=170, *args, **kwargs):
        pass

        self.mesh = obj_reader.get_mesh('Sphere', position=(x, y, -7), scale=0.1)
        self.mesh.uniforms['diffuse'] = color
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        # self.sound = pyglet.media.load('PPB.wav', streaming=False)
        pyglet.clock.schedule(self.update)

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