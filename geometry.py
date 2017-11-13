import ratcave as rc
import pyglet
import numpy as np

def sind(angle):
    return np.sin(angle*np.pi/180)

def cosd(angle):
    return np.cos(angle*np.pi/180)

obj_filename = rc.resources.obj_primitives
obj_reader = rc.WavefrontReader(obj_filename)

class Geometry(object):

    def __init__(self, mesh, x, y, speed=0, scale=1, color=(1, 1, 1)):

        self.mesh = obj_reader.get_mesh(mesh, position=(0, 0, -7), scale=scale)
        self.mesh.uniforms['diffuse'] = color
        self.speed = speed
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val
        self.mesh.position.x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val
        self.mesh.position.y = val

    @property
    def xyz(self):
        return tuple(self.mesh.position.xyz)


class Bat(Geometry):

    def __init__(self, x, y, color=(1, 1, 1), scale=0.5, speed=10, control_keys=None):
        super().__init__(mesh="Cube", x=x, y=y, color=color, scale=1, speed=speed)

        self.control_keys = control_keys

        # change the size of any dimension of the object
        self.mesh.arrays[0][:, 0:3] *= scale
        self.mesh.arrays[0][:, 0] *= 0.05  # x-dimension
        self.mesh.arrays[0][:, 1] *= 1.5  # y-dimension
        self.length_x = 2 * np.mean((abs(np.min(self.mesh.arrays[0][:, 0])), np.max(self.mesh.arrays[0][:, 0])))
        self.length_y = 2 * np.mean((abs(np.min(self.mesh.arrays[0][:, 1])), np.max(self.mesh.arrays[0][:, 1])))

    def did_bounce(self, ball_xyz, ball_radius, upper_wall_y, lower_wall_y):

        # left, right, up, down, left hit angle increment, right hit angle increment
        did_bounce_result = [False, False, False, False, 0, 0]
        boundary_y = (self.y - self.length_y/2, self.y + self.length_y/2)

        # check for the collision of the ball and the bat within the y-range of the bat
        if (ball_xyz[1] > boundary_y[0]) and (ball_xyz[1] < boundary_y[1]):

            # this is both ball and bat are in the left half of the field
            if (ball_xyz[0] < 0) and (self.x < 0) and ((ball_xyz[0] - ball_radius) < self.x + self.length_x/2) \
                    and ((ball_xyz[0] + ball_radius) > self.x - self.length_x/2):

                did_bounce_result[0] = True
                did_bounce_result[4] = (ball_xyz[1] - self.y) / self.length_y * 2 * 20

            # this is both ball and bat are in the left half of the field
            if (ball_xyz[0] > 0) and (self.x > 0) and ((ball_xyz[0] + ball_radius) > self.x - self.length_x/2) \
                    and ((ball_xyz[0] - ball_radius) < self.x + self.length_x/2):

                did_bounce_result[1] = True
                did_bounce_result[5] = -(ball_xyz[1] - self.y) / self.length_y * 2 * 20

        # upper wall (y is +ve)
        if (ball_xyz[1] + ball_radius) > upper_wall_y:
            did_bounce_result[2] = True

        # bottom wall (y is -ve)
        if (ball_xyz[1] - ball_radius) < lower_wall_y:
            did_bounce_result[3] = True

        return did_bounce_result


class Ball(Geometry):

    def __init__(self, x, y, angle, color=(1, 1, 1), scale=0.1, speed=10, sound_path=None):
        super().__init__(mesh="Sphere", x=x, y=y, color=color, scale=1, speed=speed)

        self.angle = angle
        self.speed = speed
        # self.sound = pyglet.media.load(sound_path, streaming=False)

        # change the size in any dimension
        self.mesh.arrays[0][:, 0:3] *= scale

        # calculate the radius of the ball
        self.radius = np.mean((abs(np.min(self.mesh.arrays[0][:, 0])), np.max(self.mesh.arrays[0][:, 0])))

    def update_angle(self, result, dt):

        if result[0] or result[1]:
            self.angle = 180 - self.angle + result[4] + result[5]
            # self.sound.play()

        if result[2] or result[3]:
            self.angle = 360 - self.angle
            # self.sound.play()

        # print(ball_angle)
        self.x += self.speed * cosd(self.angle) * dt
        self.y += self.speed * sind(self.angle) * dt
