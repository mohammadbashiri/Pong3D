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
path_arena = r"D:\TUM\Work\Sirota\MyModels\arena\myArena\MyArenaInComp.obj"
object = rc.WavefrontReader(path_arena)
arena_pos = [0, 0, -7]
arena = object.get_mesh('Arena', position=(arena_pos[0], arena_pos[1], arena_pos[2]), rotation=(90, 0, 0), scale=1)

# Add the bats
bat1_control_keys = (key.A, key.D, key.W, key.S)
bat2_control_keys = (key.LEFT, key.RIGHT, key.UP, key.DOWN)
x, y, z = arena.position.xyz
bat1 = Bat(x=x - 4, y=y, z=z, color=(0.6, 0, 0), control_keys=bat1_control_keys)
bat2 = Bat(x=x + 4, y=y, z=z, color=(0.6, 0, 0), control_keys=bat2_control_keys)

# Add the ball
x = np.random.randint(bat1.x+1, bat2.x+-1)
y = arena.position.y + np.random.rand() # arena boundaries (top, bottom)
angle = np.random.randint(150, 210)
ball1 = Ball(x=x, y=y, z=z, angle=angle, color=(1, 1, 1), speed=3, sound_path='PPB.wav')

# Create Scene
scene = rc.Scene(meshes=[ball1.mesh, bat1.mesh, bat2.mesh, arena])
scene.bgColor = 0, 0, 0.2  # set the background of thee scene
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
scene.camera.position.x = 0  # 0.05
scene.camera.projection.z_far = 10
scene.light.position.xyz = 0, 0, 0

arena_pos_old = arena.position.xyz

def update(dt):

    # keep track of the changes in the arena position
    global arena_pos_old
    arena_pos_change = np.array(list(arena.position.xyz)) - arena_pos_old
    arena_pos_old = arena.position.xyz
    print(arena_pos_change)

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

        # update bat position
        bb.xyz += arena_pos_change
        bb.xyz += arena_pos_change

    if keys[key.SPACE] or ball1.xyz[0] < -4 or ball1.xyz[0] > 4:
        ball1.x = arena.position.x
        ball1.y = arena.position.y + np.random.rand() - 0.5
        ball1.angle = np.random.randint(150, 210)

    # changing arena position
    if keys[key.C]:
        arena.position.x += 0.2
    elif keys[key.V]:
        arena.position.x -= 0.2

    # toggle between camera position for left and right eyes
    # scene.camera.position.x = 0 - scene.camera.position.x
    # print(bat1.x, bat1.y)
    # print(np.min(bat1.mesh.arrays[0][:, 2]), np.max(bat1.mesh.arrays[0][:, 2]))

pyglet.clock.schedule(update)
shader = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()