import pyglet
import numpy as np
from pyglet.window import key
import ratcave as rc


def sind(angle):
    return np.sin(angle*np.pi/180)

def cosd(angle):
    return np.cos(angle*np.pi/180)

# Create Window and Add Keyboard State Handler to it's Event Loop
window = pyglet.window.Window(resizable=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Insert filename into WavefrontReader.
obj_filename = rc.resources.obj_primitives # this is the path to the obj_primitives .obj file
obj_reader   = rc.WavefrontReader(obj_filename) # using the WavefrontReader read the .obj file


# Add the "bat"
bat_position = (-4, 0, -7)
bat = obj_reader.get_mesh("Cube", position = bat_position, scale= .5)
bat.uniforms['diffuse'] = 0.6, 0, 0

# Add the "bat"
bat2_position = (4, 0, -7)
bat2 = obj_reader.get_mesh("Cube", position = bat2_position, scale= .5)
bat2.uniforms['diffuse'] = 0.6, 0, 0

# Add the ball
# initialize the movement of the ball
ball_position = (np.random.randint(bat_position[1]+1,3), np.random.randint(-3.5,3.5), -7)
ball = obj_reader.get_mesh("Sphere", position = ball_position, scale= .1)
ball.uniforms['diffuse'] = 1, 1, 1

ball_angle = np.random.randint(150,210)
print(ball_angle, sind(ball_angle))
ball_speed = 5

ball_sound = pyglet.media.load('PPB.wav', streaming=False)

# Create Scene
scene = rc.Scene(meshes=[ball, bat, bat2])
scene.bgColor = 0, 0, 0.2 # set the background of thee scene
# scene.light.position.xyz = 0, 0, -9
scene.camera = rc.Camera(position=(0, 0, 0), rotation=(0, 0, 0))
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

def ball_update(dt):
    global ball_speed

    result = checkBounce(ball.position.xyz, .1, bat.position.xyz, 1)
    # result = checkBounce(ball.position.xyz, .1, bat2.position.xyz, 1)

    global ball_angle
    if result[0]==0:
        ball_angle = 180 - ball_angle
        ball_sound.play()

    if result[1]==0:
        ball_angle = 180 - ball_angle
        ball_sound.play()

    if result[2]==0:
        ball_angle = 360 - ball_angle
        ball_sound.play()

    if result[3]==0:
        ball_angle = 360 - ball_angle
        ball_sound.play()

    # print(ball_angle)
    ball.position.x += ball_speed * cosd(ball_angle) * dt
    ball.position.y += ball_speed * sind(ball_angle) * dt

pyglet.clock.schedule(ball_update)

def ball2_update(dt):
    global ball_speed

    result = checkBounce(ball.position.xyz, .1, bat2.position.xyz, 1)

    global ball_angle
    if result[0]==0:
        ball_angle = 180 - ball_angle
        ball_sound.play()

    if result[1]==0:
        ball_angle = 180 - ball_angle
        ball_sound.play()

    if result[2]==0:
        ball_angle = 360 - ball_angle
        ball_sound.play()

    if result[3]==0:
        ball_angle = 360 - ball_angle
        ball_sound.play()

    # print(ball_angle)
    ball.position.x += ball_speed * cosd(ball_angle) * dt
    ball.position.y += ball_speed * sind(ball_angle) * dt

pyglet.clock.schedule(ball2_update)

def bat_update(dt):
    bat_speed = 10

    if keys[key.A]:
        bat.position.x -= bat_speed * dt
    if keys[key.D]:
        bat.position.x += bat_speed * dt
    if keys[key.W]:
        bat.position.y += bat_speed * dt
    if keys[key.S]:
        bat.position.y -= bat_speed * dt

pyglet.clock.schedule(bat_update)

def bat2_update(dt):
    bat2_speed = 10

    if keys[key.LEFT]:
        bat2.position.x -= bat2_speed * dt
    if keys[key.RIGHT]:
        bat2.position.x += bat2_speed * dt
    if keys[key.UP]:
        bat2.position.y += bat2_speed * dt
    if keys[key.DOWN]:
        bat2.position.y -= bat2_speed * dt

pyglet.clock.schedule(bat2_update)


shader = rc.Shader.from_file(*rc.resources.genShader)

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()