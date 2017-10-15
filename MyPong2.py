import pyglet
from pyglet.window import key
import ratcave as rc

# Create Window and Add Keyboard State Handler to it's Event Loop
window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Insert filename into WavefrontReader.
obj_filename = rc.resources.obj_primitives # this is the path to the obj_primitives .obj file
obj_reader   = rc.WavefrontReader(obj_filename) # using the WavefrontReader read the .obj file

# Create Mesh
ball = obj_reader.get_mesh("Sphere", position = (0, 0, -3),     scale=.2)
ball.uniforms['diffuse'] = 1, 0, 0

# Create Scene
scene = rc.Scene(meshes=[ball])
scene.bgColor = 0, 0, 0.2 # set the background of thee scene


def ball_update(dt):
    ball_speed = 10
    if keys[key.LEFT]:
        ball.position.x -= ball_speed * dt
    if keys[key.RIGHT]:
        ball.position.x += ball_speed * dt

pyglet.clock.schedule(ball_update)


shader = rc.Shader.from_file(*rc.resources.genShader)

@window.event
def on_draw():
    with shader:
        scene.draw()

pyglet.app.run()