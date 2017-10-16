import pyglet
import numpy as np
from pyglet.window import key
import ratcave as rc
from bat import Bat
from ball import Ball


def sind(angle):
    return np.sin(angle*np.pi/180)

def cosd(angle):
    return np.cos(angle*np.pi/180)

# Create Window and Add Keyboard State Handler to it's Event Loop
window = pyglet.window.Window(resizable=True, fullscreen=False)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Insert filename into WavefrontReader.
obj_filename = rc.resources.obj_primitives # this is the path to the obj_primitives .obj file
obj_reader   = rc.WavefrontReader(obj_filename) # using the WavefrontReader read the .obj file

# Add the "bat"
bat = Bat(x=-4, y=0, color=(0.6, 0, 0))
bat2 = Bat(x=4, y=0, color=(0.6, 0, 0))

# Add the ball
# initialize the movement of the ball
x = np.random.random() * 6 - 3
y = np.random.randint(-3, 3)
angle = np.random.randint(150,210)
ball = Ball(x=x, y=y, color=(0.6, 0, 0), angle=angle)


print(ball.angle, sind(ball.angle))

#ball_sound = pyglet.media.load('PPB.wav', streaming=False)

# Create Scene
scene = rc.Scene(meshes=[ball.mesh, bat.mesh, bat2.mesh])
scene.bgColor = 0, 0, 0.2 # set the background of thee scene
# scene.light.position.xyz = 0, 0, -9
scene.camera = rc.Camera(position=(0, 0, 2), rotation=(0, 0, 0))
scene.camera.projection.z_far = 10

'''
there is a need for a function that gives the dimension of the object and its position withing
the scene in terms of pixels, because then it's much easier to relate it to the window size
'''

'''
can I change the width and height of the cube here?
'''


def checkBounce(ballPos, ballRadius, batPos, batDim):

    result = [1, 1, 1, 1] # left, right, up, down

    # left side (x is -ve)
    boundaryX = (batPos[0] - batDim/2, batPos[0] + batDim/2) # (left, right)
    boundaryY = (batPos[1] + batDim/2, batPos[1] - batDim/2) # (upper boundary, lower boundary)
    if ((ballPos[1] - ballRadius) < boundaryY[0]) and ((ballPos[1] + ballRadius) > boundaryY[1]) and batPos[0] < ballPos[0]:
        if (ballPos[0] - ballRadius) < boundaryX[1]:
            result[0] = 0

    elif (ballPos[0] - ballRadius) < -5:
        result[0] = 0

    # right side (x is +ve)
    if ((ballPos[1] - ballRadius) < boundaryY[0]) and ((ballPos[1] + ballRadius) > boundaryY[1]) and batPos[0] > ballPos[0]:
        if (ballPos[0] + ballRadius) > boundaryX[0]:
            result[1] = 0

    elif (ballPos[0] + ballRadius) > 5:
        result[1] = 0

    # upper side (y is +ve)
    if (ballPos[1] + ballRadius) > 4:
        result[2] = 0

    # bottom side (y is -ve)
    if (ballPos[1] - ballRadius) < -4:
        result[3] = 0

    return result

def ball_bounce(dt):

    for bb in [bat, bat2]:
        result = checkBounce(ball.xyz, .1, bb.xyz, 1)

        if result[0] == 0 or result[1] == 0:
            ball.bounce(True)
        if result[2] == 0 or result[3] == 0:
            ball.bounce(False)

pyglet.clock.schedule(ball_bounce)


def check_keyboard(dt):
    if keys[key.A]:
        bat.x -= bat.speed * dt
    if keys[key.D]:
        bat.x += bat.speed * dt
    if keys[key.W]:
        bat.y += bat.speed * dt
    if keys[key.S]:
        bat.y -= bat.speed * dt
    if keys[key.LEFT]:
        bat2.x -= bat2.speed * dt
    if keys[key.RIGHT]:
        bat2.x += bat2.speed * dt
    if keys[key.UP]:
        bat2.y += bat2.speed * dt
    if keys[key.DOWN]:
        bat2.y -= bat2.speed * dt
    if keys[key.SPACE]:
        globals()['ball'] = Ball(x, y, color=(0.6, 0, 0), angle=angle)

pyglet.clock.schedule(check_keyboard)

shader = rc.Shader.from_file(*rc.resources.genShader)

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()