import pyglet
# pyglet.options['debug_gl_trace'] = False
# pyglet.options['debug_gl'] = False
import numpy as np
from pyglet.window import key, FPSDisplay
import ratcave as rc
from geometry import Bat, Ball
import natnetclient as natnet

client = natnet.NatClient()
rbbat1 = client.rigid_bodies['batMotive1'] # name of rigid body in Motive

# Create Window and Add Keyboard State Handler to its Event Loop
window = pyglet.window.Window(resizable=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Add the bats
bat1_control_keys = (key.A, key.D, key.W, key.S)
bat2_control_keys = (key.LEFT, key.RIGHT, key.UP, key.DOWN)

bat1 = Bat(x=-4, y=0, color=(0.6, 0, 0), control_keys=bat1_control_keys)
# bat2 = Bat(x=4, y=0, color=(0.6, 0, 0), control_keys=bat2_control_keys)
bat3 = Bat(x=4, y=0, color=(0.6, 0, 0), control_keys=None)

# Add the ball
x = np.random.randint(bat1.x+1, bat3.x+-1)
y = np.random.randint(-3, 3)
angle = np.random.randint(150, 210)
ball1 = Ball(x=x, y=y, angle=angle, color=(1, 1, 1), speed=2, sound_path=None)

# Create Scene
scene = rc.Scene(meshes=[ball1.mesh, bat1.mesh, bat3.mesh])
scene.bgColor = 0, 0, 0.2  # set the background of thee scene
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
scene.camera.projection.z_far = 10
# scene.light.position.xyz = 0, 0, -9

fps_text = FPSDisplay(window)

def update(dt):

    for bb in [bat3]:  # rigid-body controlled bat(s)

        bb.x = -rbbat1.position[0]*10
        bb.y = rbbat1.position[2]*30
        result = bb.did_bounce(ball1.xyz, ball1.radius, 4, -4)
        ball1.update_angle(result, dt)

    for bb in [bat1]:  # keyboard controlled bat(s)
        # result = did_bounce(ball1.xyz, ball1.radius, bb.xyz, 1)

        if keys[bb.control_keys[0]]:
            bb.x -= bb.speed * dt
        if keys[bb.control_keys[1]]:
            bb.x += bb.speed * dt
        if keys[bb.control_keys[2]]:
            bb.y += bb.speed * dt
        if keys[bb.control_keys[3]]:
            bb.y -= bb.speed * dt

        result = bb.did_bounce(ball1.xyz, ball1.radius, 4, -4)
        ball1.update_angle(result, dt)

        if keys[key.SPACE] or ball1.xyz[0] < -5 or ball1.xyz[0] > 5:
            ball1.x = np.random.randint(bat1.x+1, bat3.x+-1)
            ball1.y = np.random.randint(-3, 3)
            ball1.angle = np.random.randint(150, 210)

pyglet.clock.schedule(update)
shader = rc.Shader.from_file(*rc.resources.genShader)


@window.event
def on_draw():
    with shader:
        scene.draw()
    fps_text.draw()

pyglet.app.run()