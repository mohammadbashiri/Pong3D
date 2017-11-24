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
obj_reader = rc.WavefrontReader(path_arena)
arena_pos = [0, 0, -1.5]
arena = obj_reader.get_mesh('Arena', position=(arena_pos[0], arena_pos[1], arena_pos[2]), rotation=(90, 0, 0), scale=1)
arena.uniforms['diffuse'] = (0.4, 0.4, 0.4)

# Add the bats
bat1_control_keys = (key.A, key.D, key.W, key.S)
bat2_control_keys = (key.LEFT, key.RIGHT, key.UP, key.DOWN)
bat1 = Bat(x=-0.8, y=0, color=(1, 0, 0), speed=1.5, control_keys=bat1_control_keys, rotation=(90, 0, 0))
bat2 = Bat(x=0.8, y=0, color=(1, 0, 0), speed=1.5, control_keys=bat2_control_keys, rotation=(90, 0, 0))

# Add the ball
x = 0  # np.random.randint(bat1.x+1, bat2.x+-1)
y = 0  # np.random.randint(-3, 3)
angle = np.random.randint(150, 210)
ball1 = Ball(x=x, y=y, angle=angle, color=(1, 0.5, 0), speed=0.5, sound_path='PPB.wav')

# Create Scene
scene = rc.Scene(meshes=[arena, ball1.mesh, bat1.mesh, bat2.mesh])
scene.bgColor = 0, 0, 0.2  # set the background of thee scene
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
scene.camera.projection.z_far = 10
# scene.light.position.xyz = 0, 0, -9

# saving the arena position
arena_pos_old = arena.position.xyz


def update(dt):

    # keep track of the changes in the arena position
    global arena_pos_old
    arena_pos_change = np.array(list(arena.position.xyz)) - arena_pos_old
    arena_pos_old = arena.position.xyz
    # print(arena_pos_change)

    for bb in [bat1, bat2]:

        result = bb.did_bounce(ball1.xyz, ball1.radius, 0.38 + arena.position.y, -0.38 + arena.position.y)
        ball1.update_angle(result, dt)

        if keys[bb.control_keys[0]]:
            bb.x -= bb.speed * dt
        if keys[bb.control_keys[1]]:
            bb.x += bb.speed * dt
        if keys[bb.control_keys[2]]:
            bb.y += bb.speed * dt
        if keys[bb.control_keys[3]]:
            bb.y -= bb.speed * dt

        # update bats and ball position
        bb.xyz += arena_pos_change
        bb.xyz += arena_pos_change
        ball1.xyz += arena_pos_change

        # create a new ball
        if keys[key.SPACE] or ball1.xyz[0] < -1 or ball1.xyz[0] > 1:
            ball1.x = arena.position.x  # np.random.randint(bat1.x+1, bat2.x+-1)
            ball1.y = arena.position.y  # np.random.randint(-3, 3)
            ball1.angle = np.random.randint(150, 210)

        # changing arena position
        if keys[key.C]:
            arena.position.y += 0.002
        elif keys[key.V]:
            arena.position.y -= 0.002

pyglet.clock.schedule(update)
shader = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()