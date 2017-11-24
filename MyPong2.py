import pyglet
import numpy as np
from pyglet.window import key
import ratcave as rc
from geometry import Bat, Ball

# Create Window and Add Keyboard State Handler to its Event Loop
window = pyglet.window.Window(resizable=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# add the arena assets
path_arena = r"D:\TUM\Work\Sirota\MyModels\Pong3DAssets\pongAssets.obj"
object = rc.WavefrontReader(path_arena)
arena_pos = [0, 0, -1.5]
arena = object.get_mesh('Arena', position=(arena_pos[0], arena_pos[1], arena_pos[2]), rotation=(90, 0, 0), scale=1)

# Add the bats
bat1_control_keys = (key.A, key.D, key.W, key.S)
bat2_control_keys = (key.LEFT, key.RIGHT, key.UP, key.DOWN)
bat1 = Bat(x=-0.8, y=0, color=(0.6, 0, 0), speed=1.5, control_keys=bat1_control_keys, rotation=(90, 0, 0))
bat2 = Bat(x=0.8, y=0, color=(0.6, 0, 0), speed=1.5, control_keys=bat2_control_keys, rotation=(90, 0, 0))

# Add the ball
x = 0  # np.random.randint(bat1.x+1, bat2.x+-1)
y = 0  # np.random.randint(-3, 3)
angle = np.random.randint(150, 210)
ball1 = Ball(x=x, y=y, angle=angle, color=(1, 1, 1), speed=0.5, sound_path='PPB.wav')

# Create Scene
scene = rc.Scene(meshes=[arena, ball1.mesh, bat1.mesh, bat2.mesh])
scene.bgColor = 0, 0, 0.2  # set the background of thee scene
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
scene.camera.projection.z_far = 10
# scene.light.position.xyzs = 0, 0, -9


def update(dt):

    for bb in [bat1, bat2]:

        result = bb.did_bounce(ball1.xyz, ball1.radius, 0.38, -0.38)
        ball1.update_angle(result, dt)

        if keys[bb.control_keys[0]]:
            bb.x -= bb.speed * dt
        if keys[bb.control_keys[1]]:
            bb.x += bb.speed * dt
        if keys[bb.control_keys[2]]:
            bb.y += bb.speed * dt
        if keys[bb.control_keys[3]]:
            bb.y -= bb.speed * dt

        if keys[key.SPACE] or ball1.xyz[0] < -1 or ball1.xyz[0] > 1:
            ball1.x = 0  # np.random.randint(bat1.x+1, bat2.x+-1)
            ball1.y = 0  # np.random.randint(-3, 3)
            ball1.angle = np.random.randint(150, 210)

        # print(bat1.y, arena.arrays[0][1])
        # bat2.y = arena.arrays[0][1][3]

pyglet.clock.schedule(update)
shader = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()