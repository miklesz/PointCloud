# Standard library imports
from math import *
import platform
import sys

# Related third party imports
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpPosHprInterval
# from direct.particles.ForceGroup import ForceGroup
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
# from panda3d.core import Filename
from panda3d.physics import LinearNoiseForce
from direct.particles.ForceGroup import ForceGroup
from direct.particles.Particles import Particles
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
# from panda3d.physics import DiscEmitter
# from panda3d.physics import LinearJitterForce, LinearRandomForce
# from panda3d.physics import PointParticleFactory, SpriteParticleRenderer

# Globals
current_modes_and_filters = {}

# Constants
VERBOSE = True
# VERBOSE = False
PRESET_0 = {
    'bloom': False, 'bloom_intensity': 1.0,
    'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
    'cartoon_ink': False, 'cartoon_ink_separation': 1,
    'render_mode_perspective': False,
    'render_mode_thickness': 1,
}
PRESET_1 = {
    'bloom': False, 'bloom_intensity': 1.0,
    'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
    'cartoon_ink': True, 'cartoon_ink_separation': 2,
    'render_mode_perspective': False,
    'render_mode_thickness': 10,
}
PRESET_2 = {
    'bloom': True, 'bloom_intensity': 1.0,
    'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
    'cartoon_ink': False, 'cartoon_ink_separation': 1,
    'render_mode_perspective': False,
    'render_mode_thickness': 2,
}
PRESET_3 = {
    'bloom': True, 'bloom_intensity': 0.5,
    'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
    'cartoon_ink': False, 'cartoon_ink_separation': 1,
    'render_mode_perspective': False,
    'render_mode_thickness': 3,
}
PRESET_4 = {
    'bloom': False, 'bloom_intensity': 0.0,
    'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
    'cartoon_ink': True, 'cartoon_ink_separation': 1,
    'render_mode_perspective': True,
    'render_mode_thickness': 40,
}


def change_mode_or_filter(mode_or_filter, change):
    if change is None:
        current_modes_and_filters[mode_or_filter] ^= True
    else:
        current_modes_and_filters[mode_or_filter] += change
    set_modes_and_filters()


def set_modes_and_filters(preset=None):
    global current_modes_and_filters
    if preset:
        current_modes_and_filters = preset
    print(current_modes_and_filters)
    if current_modes_and_filters['bloom']:
        filters.set_bloom(blend=(0.3, 0.4, 0.3, 1.0),
                          mintrigger=0.0,
                          desat=0,
                          intensity=current_modes_and_filters['bloom_intensity'],
                          size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
    else:
        filters.del_bloom()
    if current_modes_and_filters['blur_sharpen']:
        filters.set_blur_sharpen(amount=current_modes_and_filters['blur_sharpen_amount'])
    else:
        filters.del_blur_sharpen()
    if current_modes_and_filters['cartoon_ink']:
        filters.set_cartoon_ink(separation=current_modes_and_filters['cartoon_ink_separation'])
    else:
        filters.del_cartoon_ink()
    base.render.set_render_mode_perspective(current_modes_and_filters['render_mode_perspective'], 1)
    if current_modes_and_filters['render_mode_perspective']:
        base.render.set_render_mode_thickness(current_modes_and_filters['render_mode_thickness']/1000)
    else:
        base.render.set_render_mode_thickness(current_modes_and_filters['render_mode_thickness'])


def toggle_pos_intervals():
    """Toggle position intervals"""
    global pos_intervals
    if pos_intervals:
        sequence.finish()
        pos_intervals = False
    else:
        sequence.start()
        pos_intervals = True


def toggle_fullscreen():
    global fullscreen
    # props.setUndecorated(True)
    # props.set_fullscreen(True)
    # print('size:', local_props.has_fixed_size())
    local_props = WindowProperties()
    if fullscreen:
        local_props.set_size(1280, 720)
        local_props.setOrigin((-2, -2))
        fullscreen = False
    else:
        local_props.set_size(base.pipe.get_display_width(), base.pipe.get_display_height())
        local_props.setOrigin((0, 0))
        fullscreen = True
    base.win.request_properties(local_props)


def toggle_volume():
    music.set_volume(float(not music.get_volume()))


def beat(t):
    fov = cos(t * 30) * (1 - t) * 10 + 100  # sin
    base.camLens.setFov(fov)
    # print('beat', t)


# def beat_start(task):
#     global beat_count
#     # print('beat start', self.beat_start)
#     beat_count += 1
#     # beat_interval.start()
#     # return task  # Unnecessary
#     # return task


def accept():
    base.accept('escape', sys.exit)
    base.accept('v', toggle_volume)
    base.accept('f', toggle_fullscreen)
    base.accept('m', move_to_random)
    base.accept('b', beat_interval.start)
    base.accept('o', toggle_pos_intervals)
    base.accept('shift-b', change_mode_or_filter, ['bloom', None])
    base.accept('shift-0', change_mode_or_filter, ['bloom_intensity', +0.1])
    base.accept('shift-9', change_mode_or_filter, ['bloom_intensity', -0.1])
    base.accept('shift-c', change_mode_or_filter, ['cartoon_ink', None])
    base.accept('shift-.', change_mode_or_filter, ['cartoon_ink_separation', +1])
    base.accept('shift-,', change_mode_or_filter, ['cartoon_ink_separation', -1])
    base.accept('shift-u', change_mode_or_filter, ['blur_sharpen', None])
    base.accept('shift-]', change_mode_or_filter, ['blur_sharpen_amount', +0.1])
    base.accept('shift-[', change_mode_or_filter, ['blur_sharpen_amount', -0.1])
    base.accept(']', change_mode_or_filter, ['render_mode_thickness', +1])
    base.accept('[', change_mode_or_filter, ['render_mode_thickness', -1])
    base.accept('p', change_mode_or_filter, ['render_mode_perspective', None])
    base.accept('0', set_modes_and_filters, [PRESET_0])
    base.accept('1', set_modes_and_filters, [PRESET_1])
    base.accept('2', set_modes_and_filters, [PRESET_2])
    base.accept('3', set_modes_and_filters, [PRESET_3])
    base.accept('4', set_modes_and_filters, [PRESET_4])
    base.accept('s', start_steam)


def main_task(task):
    global lasts
    global max_delta
    global text_object

    # Onscreen text
    text = f'''\
Yo FuCkErS!
time: {str(round(music.getTime(), 2))}
escape: sys.exit

# Setting Volume
v: toggle volume (now: {music.get_volume()})

# Window Properties
f: toggle full-screen (now: {fullscreen})

# Render Modes
p: toggle render mode perspective (now: {current_modes_and_filters['render_mode_perspective']})
]/[: inc/dec render mode thickness (now: {current_modes_and_filters['render_mode_thickness']})

# Common Filters
B: toggle bloom (now: {current_modes_and_filters['bloom']})
C: toggle cartoon ink (now: {current_modes_and_filters['cartoon_ink']})
U: toggle blur/sharpen (now: {current_modes_and_filters['blur_sharpen']})
)/(: inc/dec bloom intensity (now: {round(current_modes_and_filters['bloom_intensity'], 1)})
>/<: inc/dec cartoon ink separation (now: {current_modes_and_filters['cartoon_ink_separation']})
{{/}}: inc/dec blur/sharpen (now: {current_modes_and_filters['blur_sharpen_amount']})

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

# Effects
m: set random position (once)
o: set random position (now: {pos_intervals})
b: beat (once)
s: steam (once)
'''
    if 'text_object' in globals():
        text_object.destroy()
    # pos=(-1.60, +.96)
    # pos=(-1.77, +.96)
    text_object = OnscreenText(text=text,
                               pos=(-1.77, +.96),
                               fg=(1, 1, 0, 1),
                               bg=(0, 0, 0, .5),
                               scale=0.05,
                               align=TextNode.ALeft)
    # OnscreenText(text=text,
    #                            pos=(-1.77, +.96),
    #                            fg=(1, 1, 0, 1),
    #                            bg=(0, 0, 0, .5),
    #                            scale=0.05,
    #                            align=TextNode.ALeft)

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

    # Box force
    # print(task.time)
    # global p
    # global has_force
    # if task.time > 6 and not has_force:
    #     # p.removeAllForces()
    #     f0 = ForceGroup('vertex')
    #     force0 = LinearNoiseForce(0.1500, 0)
    #     # force0 = LinearJitterForce(0.1500, 0)
    #     force0.setActive(1)
    #     f0.addForce(force0)
    #     p.softStop()
    #     p.addForceGroup(f0)
    #     has_force = True
    #     print("Force added!")
    #     print(type(p))

    return Task.cont


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


def init_steam():
    global current_modes_and_filters
    litter_size = 200
    particle_effect = ParticleEffect()
    particles = Particles('steam')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(current_modes_and_filters['render_mode_thickness'])
    particles.set_emitter("BoxEmitter")
    particles.setPoolSize(litter_size*60*8)
    particles.setBirthRate(1/60)
    particles.setLitterSize(litter_size)
    # Factory parameters
    particles.factory.set_lifespan_base(8)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    particles.renderer.set_user_alpha(0.45)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.3800))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))
    # Box parameters
    particles.emitter.set_min_bound((-2.89104, -2.71256, -1.75318))
    particles.emitter.set_max_bound((2.76295, 2.03709, -1.75318))
    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('vertex')
    # Force parameters
    linear_noise_force = LinearNoiseForce(0.1500, 0)
    linear_noise_force.setActive(True)
    force_group.addForce(linear_noise_force)
    particle_effect.add_force_group(force_group)
    return particle_effect


def start_steam():
    steam_interval = ParticleInterval(
        particleEffect=init_steam(),
        parent=model,
        worldRelative=True,
        duration=16,
        softStopT=8,
        cleanup=True,
        name='steam'
    )
    steam_interval.start()


# Init ShowBase
base = ShowBase()

has_force = False

# Print platform
if VERBOSE:
    print('platform.python_version:', platform.python_version())
    print('platform.machine:', platform.machine())

# Print base.win.gsg
if VERBOSE:
    print('base.win.gsg.driver_vendor:', base.win.gsg.driver_vendor)
    print('base.win.gsg.driver_renderer:', base.win.gsg.driver_renderer)
    print('base.win.gsg.supports_basic_shaders:', base.win.gsg.supports_basic_shaders)
    # exit()

# print PandaSystem.getVersionString()
if VERBOSE:
    print("PandaSystem.version_string:", PandaSystem.version_string)

# Load music
music = base.loader.loadSfx("music/perka.ogg")

# Set window
fullscreen = False
props = WindowProperties()
props.setIconFilename('icon-256.png')
props.setTitle('Kramsta by Damage')
base.win.request_properties(props)
toggle_fullscreen()

# Setting background color
base.setBackgroundColor(0, 0, 0)

# Load model
model = base.loader.loadModel("models/office.ply")
# model = base.loader.loadModel("models/DNA.egg")
# model = base.loader.loadModel("models/scene.gltf")
# model = base.loader.loadModel("models_other/ball.dae")
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


# Append beat intervals
beat_interval = LerpFunc(beat, fromData=0, toData=1, duration=period/4)
beat_count = 0

# Render modes and common filters
filters = CommonFilters(base.win, base.cam)
set_modes_and_filters(PRESET_0)

base.enableParticles()

base.cam.set_pos(0, -2, 0)

pos_intervals = False

# Play music
while music.status() != AudioSound.PLAYING:
    music.play()
if VERBOSE:
    print('Music time:', music.getTime())
# print('volume', music.get_volume())  # 0.0)
# print(1)
# print(float(not 1))
# exit()

# Set later tasks
# for range_time in range(16, 64, 1):
#     time = range_time * period
#     # print(time)
#     base.taskMgr.doMethodLater(time, beat_start, 'beat')

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

# On screen text object
text_object = OnscreenText()

# Accept events
accept()

# Run demo
if VERBOSE:
    print('Running demo')
    print('Music time:', music.getTime())
base.run()
