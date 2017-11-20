import pyglet
import numpy as np
from pyglet.window import key
import ratcave as rc
from geometry import Bat, Ball

# Create Window and Add Keyboard State Handler to its Event Loop
window = pyglet.window.Window(resizable=True, fullscreen=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# add the arena
path_arena = r"D:\TUM\Work\Sirota\MyModels\arena\myArena\MyArena2.obj"
object = rc.WavefrontReader(path_arena)
arena_x = 0
arena_y = 0
arena_z = -7.5
arena = object.get_mesh('Arena', position=(arena_x, arena_y, arena_z), rotation=(90, 0, 0), scale=5)

# Add the bats
bat1_control_keys = (key.A, key.D, key.W, key.S)
bat2_control_keys = (key.LEFT, key.RIGHT, key.UP, key.DOWN)
bat1 = Bat(x=arena_x-4, y=arena_y+0, z=arena_z+0.5, color=(0.6, 0, 0), control_keys=bat1_control_keys)
bat2 = Bat(x=arena_x+4, y=arena_y+0, z=arena_z+0.5, color=(0.6, 0, 0), control_keys=bat2_control_keys)

# Add the ball
x = np.random.randint(bat1.x+1, bat2.x+-1)
y = np.random.randint(-2, 2)
angle = np.random.randint(150, 210)
ball1 = Ball(x=x, y=y, z=arena_z+0.5, angle=angle, color=(1, 1, 1), speed=3, sound_path='PPB.wav')

# Create Scene
scene = rc.Scene(meshes=[ball1.mesh, bat1.mesh, bat2.mesh, arena])
scene.bgColor = 0, 0, 0.2  # set the background of thee scene
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
scene.camera.projection.z_far = 10
scene.light.position.xyz = 0, 0, 0

#
def update(dt):

    for bb in [bat1, bat2]:
        # result = did_bounce(ball1.xyz, ball1.radius, bb.xyz, 1)
        result = bb.did_bounce(ball1.xyz, ball1.radius, 2, -2)
        ball1.update_angle(result, dt)

        if keys[bb.control_keys[0]]:
            bb.x -= bb.speed * dt
        if keys[bb.control_keys[1]]:
            bb.x += bb.speed * dt
        if keys[bb.control_keys[2]]:
            bb.y += bb.speed * dt
        if keys[bb.control_keys[3]]:
            bb.y -= bb.speed * dt

        if keys[key.SPACE] or ball1.xyz[0] < -5 or ball1.xyz[0] > 5:
            ball1.x = np.random.randint(bat1.x+1, bat2.x+-1)
            ball1.y = np.random.randint(-3, 3)
            ball1.angle = np.random.randint(150, 210)

    # scene.camera.position.x += 0.1

    print(bat1.x, bat1.y)
    # print(np.min(bat1.mesh.arrays[0][:, 2]), np.max(bat1.mesh.arrays[0][:, 2]))

pyglet.clock.schedule(update)
shader = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()