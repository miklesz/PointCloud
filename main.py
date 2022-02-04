from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from panda3d.core import *
from math import *

from direct.interval.LerpInterval import LerpPosHprInterval

from panda3d.core import Filename
# from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
# from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce
# from panda3d.physics import DiscEmitter
# from panda3d.physics import LinearJitterForce, LinearRandomForce
# from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

import sys

# Set const
VERBOSE = True
# VERBOSE = False


def beat(t):
    fov = cos(t * 30) * (1 - t) * 10 + 100  # sin
    base.camLens.setFov(fov)
    # print('beat', t)


def beat_start(task):
    global beat_count
    # print('beat start', self.beat_start)
    beat_count += 1
    # beat_interval.start()
    # return task  # Unnecessary


def accept():
    base.accept('escape', sys.exit)
    base.accept('m', move_to_random)
    base.accept('b', beat_interval.start)
    base.accept('c', toggle_cartoon_ink)
    base.accept('p', toggle_render_mode_perspective)
    base.accept('o', toggle_pos_intervals)
    base.accept(']', inc_render_mode_thickness)
    base.accept('[', dec_render_mode_thickness)
    base.accept('shift-0', inc_bloom)
    base.accept('shift-9', dec_bloom)
    base.accept('shift-.', inc_separation)
    base.accept('shift-,', dec_separation)
    base.accept('shift-]', inc_blur_sharpen)
    base.accept('shift-[', dec_blur_sharpen)
    base.accept('0', preset_0)
    base.accept('1', preset_1)
    base.accept('2', preset_2)
    base.accept('3', preset_3)
    base.accept('4', preset_4)


def main_task(task):
    global lasts
    global max_delta
    global text_object
    global render_mode_thickness
    global cartoon_ink
    global bloom
    global pos_intervals
    global separation
    global blur_sharpen

    # Onscreen text
    text = f'''\
Yo FuCkErS!
time: {str(round(music.getTime(), 2))}
m: move to random position (once)
b: beat (once)
c: toggle cartoon ink (now: {cartoon_ink})
p: toggle render mode perspective (now: {base.render.get_render_mode_perspective()})
o: toggle pos intervals (now: {pos_intervals})
)/(: inc/dec bloom intensity (now: {bloom})
]/[: inc/dec render mode thickness (now: {render_mode_thickness})
>/<: inc/dec cartoon ink separation (now: {separation})
{{/}}: adjust blur/sharpen (now: {blur_sharpen})
0: set preset 0 (`None`)
1: set preset 1 (`Outdoor`)
2: set preset 2 (`Indoor 2px`)
3: set preset 3 (`Indoor 3px`)
4: set preset 4 (`Outdoor Perspective`)
5: set preset 5 (`???`)
6: set preset 6 (`???`)
7: set preset 7 (`???`)
8: set preset 8 (`???`)
9: set preset 9 (`???`)
escape: sys.exit
iddqd: ok, just joking ;-)'''
    if 'text_object' in globals():
        text_object.destroy()
    text_object = OnscreenText(text=text,
                               pos=(-1.77, +.9),
                               fg=(1, 1, 0, 1),
                               bg=(0, 0, 0, .5),
                               scale=0.05,
                               align=TextNode.ALeft)

    # decay = 1
    scale_y = 1
    model.setScale(1, scale_y, 1)

    pos = base.cam.getPos()
    currents[0] = pos[0]
    currents[1] = pos[1]
    currents[2] = pos[2]
    hpr = base.cam.getHpr()
    currents[3] = hpr[0]
    currents[4] = hpr[1]
    currents[5] = hpr[2]
    currents[6] = scale_y
    currents[7] = base.camLens.getFov()[0]

    if task.frame < 3:
        lasts = currents[:]

    for index in range(8):
        deltas[index] = currents[index] - lasts[index]

    delta = 0
    for index in range(8):
        delta += abs(deltas[index]*weights[index])

    if delta > max_delta:
        max_delta = delta

    # filters.setBlurSharpen(1 - delta)

    lasts = currents[:]

    # print(task.time)
    global p
    global has_force
    if task.time > 6 and not has_force:
        # p.removeAllForces()
        f0 = ForceGroup('vertex')
        force0 = LinearNoiseForce(0.1500, 0)
        # force0 = LinearJitterForce(0.1500, 0)
        force0.setActive(1)
        f0.addForce(force0)
        p.softStop()
        p.addForceGroup(f0)
        has_force = True
        print("Force added!")
        print(type(p))

    return Task.cont


# Init ShowBase
base = ShowBase()

has_force = False

# Print base.win.gsg
if VERBOSE:
    print('base.win.gsg.driver_vendor:', base.win.gsg.driver_vendor)
    print('base.win.gsg.driver_renderer:', base.win.gsg.driver_renderer)
    print('base.win.gsg.supports_basic_shaders:', base.win.gsg.supports_basic_shaders)

# print PandaSystem.getVersionString()
if VERBOSE:
    print("PandaSystem.version_string:", PandaSystem.version_string)

# Load music
music = base.loader.loadSfx("music/perka.ogg")

# Set window
props = WindowProperties()
props.setSize(base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight())
# props.setFixedSize(1)
props.setTitle('Amiga Rulez!')
base.win.requestProperties(props)

# Setting background color
base.setBackgroundColor(0, 0, 0)

# Load model
model = base.loader.loadModel("models/office.ply")
model.reparentTo(base.render)
if VERBOSE:
    model.ls()
    print('base.model.getTightBounds():', model.getTightBounds())
    model.analyze()

# Set frame rate meter
# base.set_frame_rate_meter = True
base.setFrameRateMeter(True)

# Point-Cloud
point_cloud = model.find("**/+GeomNode")

print(len(point_cloud.node().modify_geoms()))
for geom in point_cloud.node().modify_geoms():
    geom.make_points_in_place()
# if VERBOSE:
#     print('type(point_cloud):', type(point_cloud))
# if VERBOSE:
#     point_cloud.ls()
#     print('base.model.getTightBounds():', point_cloud.getTightBounds())
#     point_cloud.analyze()
# # quit()
#
# del point_cloud
# del model

# def create_points():
#
#     # Define GeomVertexArrayFormats for the various vertex attributes.
#
#     array = GeomVertexArrayFormat()
#     array.add_column(InternalName.make("vertex"), 3, Geom.NT_float32, Geom.C_point)
#     array.add_column(InternalName.make("color"), 4, Geom.NT_uint8, Geom.C_color)
#     array.add_column(InternalName.make("index"), 1, Geom.NT_int32, Geom.C_index)
#
#     vertex_format = GeomVertexFormat()
#     vertex_format.add_array(array)
#     vertex_format = GeomVertexFormat.register_format(vertex_format)
#
#     vertex_data = GeomVertexData("point_data", vertex_format, Geom.UH_static)
#     vertex_data.set_num_rows(8)
#
#     pos_writer = GeomVertexWriter(vertex_data, "vertex")
#     index_writer = GeomVertexWriter(vertex_data, "index")
#
#     index = 0
#
#     # create 8 points as if they were the corner vertices of a cube
#     for z in (-1., 1.):
#         for x, y in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
#             pos_writer.add_data3(x, y, z)
#             index_writer.add_data1i(index)
#             index += 1
#
#     prim = GeomPoints(Geom.UH_static)
#     prim.add_next_vertices(8)
#     geom = Geom(vertex_data)
#     geom.add_primitive(prim)
#     node = GeomNode("points_geom_node")
#     node.add_geom(geom)
#
#     return node
#
# model = base.render.attach_new_node(create_points())
# model.setRenderModeThickness(10)
# model.reparentTo(base.render)

# Set camera lens field of view
base.camLens.setFov(100)
# base.camLens.fov = 100

# Set currents, lasts, deltas and weights
currents = [0, 0, 0, 0, 0, 0, 1, base.camLens.getFov()[0]]
lasts = [0, 0, 0, 0, 0, 0, 1, base.camLens.getFov()[0]]
deltas = [0, 0, 0, 0, 0, 0, 0, 0]
weights = [.2, .2, .2, .2, .2, .2, 50, .1]
# delta = 0

# Set period
period = 120/125

# def get_pos_interval():
#     pass

# Append position intervals
dummy = base.render.attachNewNode("dummy")
sequence = Sequence()
rn = Randomizer()
old_hpr = base.cam.getHpr()
for interval_index in range(64):
    pos1 = (rn.randomRealUnit() * 4.79, rn.randomRealUnit() * 3.81, rn.randomReal(2.66 - 1.75))
    dummy.setPos(pos1)
    dummy.lookAt(0, 0, 0)
    new_hpr = dummy.getHpr()

    if new_hpr[0] - old_hpr[0] > 180:
        new_hpr[0] -= 360

    if new_hpr[0] - old_hpr[0] < -180:
        new_hpr[0] += 360

    if abs(new_hpr[0] - old_hpr[0]) > 180:
        overfull = True
    else:
        overfull = False

    # print('old_hpr:', old_hpr, 'new_hpr:', new_hpr, 'overfull:', overfull)
    old_hpr = new_hpr
    interval = LerpPosHprInterval(nodePath=base.cam,
                                  duration=period*8,
                                  pos=pos1,
                                  hpr=new_hpr,
                                  blendType='easeOut')  # period
    sequence.append(interval)


def move_to_random():
    # start_pos = base.cam.get_hpr()
    start_hpr = base.cam.get_hpr()
    pos = (rn.randomRealUnit() * 4.79, rn.randomRealUnit() * 3.81, rn.randomReal(2.66 - 1.75))
    pos_dummy = base.render.attach_new_node("pos dummy")
    pos_dummy.set_pos(pos)
    pos_dummy.look_at(0, 0, 0)
    hpr = pos_dummy.get_hpr()
    if hpr[0]-start_hpr[0] > +180:
        hpr[0] -= 360
    if hpr[0]-start_hpr[0] < -180:
        hpr[0] += 360
    random_interval = LerpPosHprInterval(nodePath=base.cam,
                                         duration=1,
                                         pos=pos,
                                         hpr=hpr,
                                         blendType='easeInOut')
    # Sequence just to avoid warnings!
    random_sequence = Sequence()
    random_sequence.append(random_interval)
    random_sequence.start()


# Append beat intervals
beat_interval = LerpFunc(beat, fromData=0, toData=1, duration=period/4)
beat_count = 0

base.enableParticles()
# Start of the code from ptf
p = ParticleEffect()
# p.loadConfig(Filename('particles/evaporation_point.ptf'))
p.loadConfig(Filename('particles/box.ptf'))
# p.loadConfig(Filename('particles/evaporation_sprite.ptf'))
p.start(parent=model)
# p.setPos(3.000, 0.000, 2.250)
p.setPos(0, 0, 0)

base.cam.set_pos(0, -2, 0)

# print(p.getForceGroupDict())
# p.removeAllForces()

# Common filters
filters = CommonFilters(base.win, base.cam)
render_mode_thickness = 1
cartoon_ink = False
bloom = 0.0
pos_intervals = False
separation = 1
blur_sharpen = 1.0


# Cartoon Ink
def toggle_cartoon_ink():
    """Toggle cartoon ink"""
    global cartoon_ink
    if cartoon_ink:
        filters.del_cartoon_ink()
        cartoon_ink = False
    else:
        filters.set_cartoon_ink()   # separation=1)
        cartoon_ink = True


def toggle_pos_intervals():
    """Toggle position intervals"""
    global pos_intervals
    if pos_intervals:
        sequence.finish()
        pos_intervals = False
    else:
        sequence.start()
        pos_intervals = True


# Bloom Intensity
def inc_bloom():
    change_bloom(step=+.1)


def dec_bloom():
    change_bloom(step=-.1)


def change_bloom(step):
    """Change bloom intensity"""
    global bloom
    bloom = round(bloom+step, 1)
    if bloom < 0.0:
        bloom = 0.0
    filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                      mintrigger=0.0,
                      desat=0,
                      intensity=bloom,
                      size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)


def toggle_render_mode_perspective():
    """Toggle render mode perspective"""
    global render_mode_thickness
    if base.render.get_render_mode_perspective():
        base.render.set_render_mode_perspective(False, 1)
        base.render.set_render_mode_thickness(render_mode_thickness)
    else:
        base.render.set_render_mode_perspective(True, 1)
        base.render.set_render_mode_thickness(render_mode_thickness/1000)


def inc_separation():
    change_separation(step=+1)


def dec_separation():
    change_separation(step=-1)


def change_separation(step):
    """Change cartoon ink separation"""
    global separation
    separation += step
    if separation == 0:
        separation = 1
    if cartoon_ink:
        filters.setCartoonInk(separation=separation)


def inc_blur_sharpen():
    change_blur_sharpen(step=+.1)


def dec_blur_sharpen():
    change_blur_sharpen(step=-.1)


def change_blur_sharpen(step):
    """Change blur/sharpen"""
    global blur_sharpen
    blur_sharpen = round(blur_sharpen+step, 1)
    filters.set_blur_sharpen(amount=blur_sharpen)


# Rendering modes
def inc_render_mode_thickness():
    change_render_mode_thickness(step=+1)


def dec_render_mode_thickness():
    change_render_mode_thickness(step=-1)


def change_render_mode_thickness(step):
    """Change render mode thickness"""
    global render_mode_thickness
    render_mode_thickness += step
    if render_mode_thickness == 0:
        render_mode_thickness = 1
    if base.render.get_render_mode_perspective():
        base.render.set_render_mode_thickness(render_mode_thickness/1000)
    else:
        base.render.set_render_mode_thickness(render_mode_thickness)


def preset_0():
    global render_mode_thickness
    global cartoon_ink
    global separation
    global blur_sharpen
    global bloom
    render_mode_thickness = 1
    base.render.set_render_mode_thickness(render_mode_thickness)
    cartoon_ink = False
    filters.del_cartoon_ink()
    blur_sharpen = 1.0
    filters.set_blur_sharpen(amount=blur_sharpen)
    bloom = 0.0
    filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                      mintrigger=0.0,
                      desat=0,
                      intensity=bloom,
                      size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
    base.render.set_render_mode_perspective(False, 1)


def preset_1():
    global render_mode_thickness
    global cartoon_ink
    global separation
    global blur_sharpen
    global bloom
    render_mode_thickness = 10
    base.render.set_render_mode_thickness(render_mode_thickness)
    cartoon_ink = True
    separation = 1
    filters.set_cartoon_ink(separation=separation)
    blur_sharpen = 1.0
    filters.set_blur_sharpen(amount=blur_sharpen)
    bloom = False
    filters.del_bloom()
    base.render.set_render_mode_perspective(False, 1)


def preset_2():
    global render_mode_thickness
    global cartoon_ink
    global blur_sharpen
    global bloom
    render_mode_thickness = 2
    base.render.set_render_mode_thickness(render_mode_thickness)
    cartoon_ink = False
    filters.del_cartoon_ink()
    blur_sharpen = 1.0
    filters.set_blur_sharpen(amount=blur_sharpen)
    bloom = True
    filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                      mintrigger=0.0,
                      desat=0,
                      intensity=1.0,
                      size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
    base.render.set_render_mode_perspective(False, 1)


def preset_3():
    global render_mode_thickness
    global cartoon_ink
    global blur_sharpen
    global bloom
    render_mode_thickness = 3
    base.render.set_render_mode_thickness(render_mode_thickness)
    cartoon_ink = False
    filters.del_cartoon_ink()
    blur_sharpen = 1.0
    filters.set_blur_sharpen(amount=blur_sharpen)
    bloom = True
    filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                      mintrigger=0.0,
                      desat=0,
                      intensity=0.5,
                      size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
    base.render.set_render_mode_perspective(False, 1)


def preset_4():
    global render_mode_thickness
    global cartoon_ink
    global separation
    global blur_sharpen
    global bloom
    render_mode_thickness = 40
    base.render.set_render_mode_thickness(render_mode_thickness/1000)
    cartoon_ink = True
    separation = 1
    filters.set_cartoon_ink(separation=separation)
    blur_sharpen = 1.0
    filters.set_blur_sharpen(amount=blur_sharpen)
    bloom = 0.0
    filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                      mintrigger=0.0,
                      desat=0,
                      intensity=bloom,
                      size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
    base.render.set_render_mode_perspective(True, 1)


# Play music
while music.status() != AudioSound.PLAYING:
    music.play()
if VERBOSE:
    print('Music time:', music.getTime())

# Set later tasks
for range_time in range(16, 64, 1):
    time = range_time * period
    # print(time)
    base.taskMgr.doMethodLater(time, beat_start, 'beat')

# Set max delta
max_delta = 0

# Add and start main task
if VERBOSE:
    print('Adding main task')
    print('Music time:', music.getTime())
base.taskMgr.add(main_task, "main_task")

# Start sequence
# sequence.start()
if VERBOSE:
    print('Starting sequence')
    print('Music time:', music.getTime())

# Accept events
accept()

# PStatClient.connect()

# Run demo
if VERBOSE:
    print('Running demo')
    print('Music time:', music.getTime())
base.run()
