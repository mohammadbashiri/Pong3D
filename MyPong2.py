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
# torus  = obj_reader.get_mesh("Torus",  position = (0, 0.5, -3),     scale=.6, rotation=(1, 90, 0))
# cube   = obj_reader.get_mesh("Cube",   position = (0, -1, -3),    scale=.6)

# Create Scene
scene = rc.Scene(meshes=[ball])
scene.bgColor = 0, 0, 0.2 # set the background of thee scene

# Functions to Run in Event Loop
# this function runs between each frame, so you will se the updated image in each frame
def rotate_meshes(dt):
    ball.rotation.y += 15 * dt  # dt is the time between frames
    # torus.rotation.y  += 500 * dt
    # cube.rotation.y   -= 200 * dt

pyglet.clock.schedule(rotate_meshes)

# you could also put a delay for the update (uncomment the following line)
# pyglet.clock.schedule_interval(rotate_meshes, .1) # update the variables every 0.1 seconds

# move the camera, using the keyboard keys (left and right arrow)
def move_camera(dt):
    camera_speed = 5
    if keys[key.LEFT]:
        scene.camera.position.x -= camera_speed * dt
    if keys[key.RIGHT]:
        scene.camera.position.x += camera_speed * dt
    if keys[key.DOWN]:
        scene.camera.position.y += camera_speed * dt
    if keys[key.UP]:
        scene.camera.position.y -= camera_speed * dt

pyglet.clock.schedule(move_camera)

# what does this do??
shader = rc.Shader.from_file(*rc.resources.genShader)

# What is this decorator for?
@window.event
def on_draw():
    with shader:
        scene.draw()


pyglet.app.run()