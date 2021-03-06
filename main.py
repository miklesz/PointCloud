# Standard library imports
from math import *
import pathlib  # Testing!
import platform
# noinspection PyUnresolvedReferences
import queue
import requests
import sys
import time
import urllib3

# Related third party imports
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpPosHprInterval
from direct.showbase.ShowBase import ShowBase
from direct.showutil.Rope import Rope
from direct.task import Task
from panda3d.core import *

# Local application/library specific imports
from particles import *

# Globals
current_modes_and_filters = {
    'color_scale': 0,
}
enable_roping = True
done = False
pos_hpr_amplitudes = [.1, .1, .1, 5, 5, 5]  # .005, .5
profile_list = []
retro_card = {}
tab_mode = False

# Constants
COLOR_SCALES = (
    ('Default', (127.5, 127.5, 127.5)),
    ('Oxford Blue', (15, 35, 71)),
    ('Rainbow Indigo', (28, 63, 110)),
    ('Lapis Lazuli', (46, 103, 160)),
    ('Carolina Blue', (90, 172, 207)),
    ('Key Lime', (239, 252, 147)),
    ('Dollar Bill', (128, 194, 113))
)
# print('sys.executable:', sys.executable)
if sys.executable == '/Users/miklesz/PycharmProjects/PointCloud/venv/bin/python':
    DEVEL = True  # True/False
else:
    DEVEL = False  # True/False
# DEVEL = False
JUMP = 264   # 5, 25, 34, 47, 84, 86, 109, 113, 150, 182, 186, 206, 238, 280
PRESETS = [
    {
        'preset': 0,
        'bloom': False, 'bloom_intensity': 1.0,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': False, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 1
    },
    {
        'preset': 1,
        'bloom': False, 'bloom_intensity': 1.0,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': True, 'cartoon_ink_separation': 2,
        'render_mode_perspective': False,
        'render_mode_thickness': 10,
    },
    {
        'preset': 2,
        'bloom': True, 'bloom_intensity': 1.0,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': False, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 2,
    },
    {
        'preset': 3,
        'bloom': True, 'bloom_intensity': 0.5,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': False, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 3,
    },
    {
        'preset': 4,
        'bloom': False, 'bloom_intensity': 0.0,
        'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': True, 'cartoon_ink_separation': 1,
        'render_mode_perspective': True,
        'render_mode_thickness': 40,
    },
    {
        'preset': 5,
        'bloom': False, 'bloom_intensity': 0.0,
        'blur_sharpen': True, 'blur_sharpen_amount': -1.5,
        'cartoon_ink': True, 'cartoon_ink_separation': 1,
        'render_mode_perspective': True,
        'render_mode_thickness': 40,
    },
    {
        'preset': 6,
        'bloom': False, 'bloom_intensity': 0.0,
        'blur_sharpen': True, 'blur_sharpen_amount': -1.5,
        'cartoon_ink': True, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 10,
    },
    {
        'preset': 7,
        'bloom': False, 'bloom_intensity': 1.0,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': True, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 10,
    },
    {
        'preset': 8,
        'bloom': False, 'bloom_intensity': 1.0,
        'blur_sharpen': False, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': False, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 10,
    },
]
RING_START = -4.2  # -5.0
RING_STOP = -0.7  # 0.0
SHAKE_DEN = 1
START = time.time()  # Start time
STILL_START = 25
STILL_STOP = 280


def change_mode_or_filter(mode_or_filter, change):
    global current_modes_and_filters
    if change is None:
        current_modes_and_filters[mode_or_filter] ^= True
    else:
        current_modes_and_filters[mode_or_filter] += change
    current_modes_and_filters['preset'] = 0  # None
    set_modes_and_filters()


def set_modes_and_filters(set_preset=None):
    global current_modes_and_filters
    global models
    if set_preset:
        # current_modes_and_filters = set_preset
        for key in set_preset:
            current_modes_and_filters[key] = set_preset[key]
    # print(current_modes_and_filters)
    # quit()
    if current_modes_and_filters['bloom']:
        filters.set_bloom(
            blend=(0.3, 0.4, 0.3, 0.0),
            mintrigger=0.0,
            maxtrigger=1.0,
            desat=0,
            intensity=current_modes_and_filters['bloom_intensity'],
            size="large"
        )  # blend=(0.3,0.4,0.3,0.0), (0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
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
        for model in models:
            models[model].set_render_mode_thickness(current_modes_and_filters['render_mode_thickness'])
            models[model].set_render_mode_perspective(current_modes_and_filters['render_mode_perspective'], 1)
    else:
        base.render.set_render_mode_thickness(current_modes_and_filters['render_mode_thickness'])
        for model in models:
            models[model].set_render_mode_thickness(current_modes_and_filters['render_mode_thickness'])
            models[model].set_render_mode_perspective(current_modes_and_filters['render_mode_perspective'], 1)
    # print(current_modes_and_filters['color_scale'])
    base.render.setColorScale(
        COLOR_SCALES[current_modes_and_filters['color_scale'] % len(COLOR_SCALES)][1][0] / 255 * 2,
        COLOR_SCALES[current_modes_and_filters['color_scale'] % len(COLOR_SCALES)][1][1] / 255 * 2,
        COLOR_SCALES[current_modes_and_filters['color_scale'] % len(COLOR_SCALES)][1][2] / 255 * 2,
        1,
    )


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
    # props.setUndecorated(False)
    # props.set_fullscreen(True)
    local_props = WindowProperties()
    # print('size:', local_props.has_fixed_size())
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
    # fov = cos(t * 30) * (1 - t) * 10 + 100  # sin
    fov = cos(t * 30) * (1 - t) * 10 + 115  # sin
    base.camLens.setFov(fov)
    # print('beat', t)

    # blur = 1 - cos(t * 30) * (1 - t)
    # print(blur)
    # current_modes_and_filters['blur_sharpen_amount'] = blur
    # set_modes_and_filters()


# def beat_start(task):
#     global beat_count
#     # print('beat start', self.beat_start)
#     beat_count += 1
#     # beat_interval.start()
#     # return task  # Unnecessary
#     # return task

def escape():
    if DEVEL:
        print('Escape pressed -> sys.exit')
        with open('profile_list.csv', 'w') as profile_file:
            for profile_time in profile_list:
                profile_file.write(f'{profile_time}\n')
    sys.exit()


def tab():
    global tab_mode
    if tab_mode:
        if DEVEL:
            print('Switching tab_mode to False')
        base.set_frame_rate_meter(False)
        tab_mode = False
    else:
        if DEVEL:
            print('Switching tab_mode to True')
        base.set_frame_rate_meter(True)
        tab_mode = True


def accept():
    base.accept('escape', escape)
    base.accept('tab', tab)
    if DEVEL:
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
        base.accept('0', set_modes_and_filters, [PRESETS[0]])
        base.accept('1', set_modes_and_filters, [PRESETS[1]])
        base.accept('2', set_modes_and_filters, [PRESETS[2]])
        base.accept('3', set_modes_and_filters, [PRESETS[3]])
        base.accept('4', set_modes_and_filters, [PRESETS[4]])
        base.accept('5', set_modes_and_filters, [PRESETS[5]])
        base.accept('6', set_modes_and_filters, [PRESETS[6]])
        base.accept('7', set_modes_and_filters, [PRESETS[7]])
        base.accept('8', set_modes_and_filters, [PRESETS[8]])
        base.accept('s', start_steam)
        base.accept('w', accept_water)
        base.accept('g', start_glow)
        base.accept('z', start_zoom)
        base.accept('d', dust_storm)
        base.accept('i', init_display_sequence)
        base.accept('a', change_mode_or_filter, ['color_scale', +1])
        base.accept('t', accept_trainspotting)
        base.accept('h', accept_handshaking)
        base.accept('r', accept_roping)
        base.accept('space', accept_roping)
        base.accept('c', accept_cubes)
        base.accept('arrow_left', accept_yaw, [+2])
        base.accept('arrow_right', accept_yaw, [-2])
        base.accept('arrow_left-repeat', accept_yaw, [+2])
        base.accept('arrow_right-repeat', accept_yaw, [-2])
        base.accept('arrow_up', accept_pitch, [+2])
        base.accept('arrow_down', accept_pitch, [-2])
        base.accept('arrow_up-repeat', accept_pitch, [+2])
        base.accept('arrow_down-repeat', accept_pitch, [-2])
        # base.accept('lshift', accept_shift, [-5])
        # base.accept('rshift', accept_shift, [+5])
        base.accept(',', accept_shift, [-5])
        base.accept('.', accept_shift, [+5])
        base.accept('e', accept_effect)
        # base.accept('j', demo_parallel.setT, [JUMP])
        base.accept('j', demo_sequence.setT, [JUMP])


def main_task(task):
    # print('I am main_task')
    global lasts
    global max_delta
    global text_object

    # Onscreen text
    text = f'''\
Yo FuCkErS!
time: {str(round(music.get_time(), 2))}
'''
    # if not demo_parallel.isPlaying():
    if not demo_sequence.isPlaying():
        text += f'''\
escape: sys.exit
space: start/stop demo (,/. to skip)
j: jump to time

# Render Modes
p: toggle render mode perspective (now: {current_modes_and_filters['render_mode_perspective']})
]/[: inc/dec render mode thickness (now: {current_modes_and_filters['render_mode_thickness']})

# Common Filters
B: toggle bloom (now: {current_modes_and_filters['bloom']})
C: toggle cartoon ink (now: {current_modes_and_filters['cartoon_ink']})
U: toggle blur/sharpen (now: {current_modes_and_filters['blur_sharpen']})
)/(: inc/dec bloom intensity (now: {round(current_modes_and_filters['bloom_intensity'], 1)})
>/<: inc/dec cartoon ink separation (now: {current_modes_and_filters['cartoon_ink_separation']})
{{/}}: inc/dec blur/sharpen (now: {round(current_modes_and_filters['blur_sharpen_amount'], 1)})

# Presets (now: {current_modes_and_filters['preset']})
0: set preset 0 (`None`)
1: set preset 1 (`Outdoor Thick`)
2: set preset 2 (`Indoor 2px`)
3: set preset 3 (`Indoor 3px`)
4: set preset 4 (`Outdoor Perspective`)
5: set preset 5 (`Sitkowy`)
6: set preset 6 (`Mikleszowy`)
7: set preset 7 (`Outdoor Thin`)
8: set preset 8 (`Mikleszowy no shader`)
9: set preset 9 (`???`)

# Motion
m: set random position (once)
o: set random position (now: {pos_intervals})
<-/-> yaw

# Effects
b: beat (once)
t: trainspotting (once)
s: steam (once)
w: water condensation (once)
z: dolly zoom (once)
d: dust storm (once)
i: display (once)
g: glowworms/fireflies (once)
h: handshaking (once)
c: cubes (once)

# Misc
a: avatarize - setting color scale (now: {COLOR_SCALES[current_modes_and_filters['color_scale'] % len(COLOR_SCALES)][0]})
v: toggle (set) volume (now: {music.get_volume()})
f: toggle full-screen - window properties (now: {fullscreen})
'''
    if 'text_object' in globals():
        text_object.destroy()
    if DEVEL or tab_mode:
        text_object = OnscreenText(text=text,  # text
                                   # pos=(-1.77, +.96),  # +.96
                                   pos=(-base.getAspectRatio(), +.97),  # +.96
                                   fg=(1, 1, 0, 1),
                                   bg=(0, 0, 0, .5),
                                   scale=0.037,  # 0.05
                                   align=TextNode.ALeft)

    # decay = 1

    # Off so as not to pertain to a model temporarily that may not be there.
    scale_y = .2
    # model.set_scale(1, scale_y, 1)
    # base.cam.set_scale(1, scale_y, 1)
    # base.cam.set_scale(1, 1, 1)

    pos = spectator.getPos()
    currents[0] = pos[0]
    currents[1] = pos[1]
    currents[2] = pos[2]
    hpr = spectator.getHpr()
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

    # Tu stare, prymitywne w????czanie motion blur
    # print(delta)
    # filters.setBlurSharpen(1 - delta*4)

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

    # if (task.dt > 0.0):
    #     print(1.0 / task.dt)

    # print(task.dt)

    return Task.cont


def accept_yaw(yaw):
    spectator.set_h(spectator.get_h()+yaw)


def accept_pitch(pitch):
    spectator.set_p(spectator.get_p()+pitch)


def init_pos_interval(pos, duration=1):
    # start_pos = base.cam.get_hpr()
    start_hpr = spectator.get_hpr()
    pos_dummy = base.render.attach_new_node("pos dummy")
    pos_dummy.set_pos(pos)
    pos_dummy.look_at(0, 0, 0)
    hpr = pos_dummy.get_hpr()
    if hpr[0]-start_hpr[0] > +180:
        hpr[0] -= 360
    if hpr[0]-start_hpr[0] < -180:
        hpr[0] += 360
    return LerpPosHprInterval(nodePath=spectator, duration=duration, pos=pos, hpr=hpr, blendType='easeInOut')


def move_to_random():
    pos = (rn.randomRealUnit() * 4.79, rn.randomRealUnit() * 3.81, rn.randomReal(2.66 - 1.75))
    # Sequence just to avoid warnings!
    random_sequence = Sequence()
    random_sequence.append(init_pos_interval(pos))
    random_sequence.start()


def start_steam():
    # r.removeNode()
    # rope_look.removeNode()
    # models['room_1'].reparent_to(base.render)
    # models['room_2'].reparent_to(base.render)
    # models['room_3'].reparent_to(base.render)
    # print(models['room_1'].getTightBounds())
    steam_interval.start()


def roping_function(t):
    global points
    global looks
    profile_list.append(music.get_time())
    # profile_list.append(len(points) * t / 5000)
    i = int(len(points)*t)-1
    if i < 0:
        i = 0
    # print(i)
    if enable_roping:
        spectator.set_pos(points[i])
        spectator.lookAt(looks[i])
    # spectator.lookAt(0, 0, 0)


def model_function(model, add):
    global models
    if add:
        print(f'model_dict[model][\'{model}\'].reparentTo(base.render)')
        models[model].reparentTo(base.render)
    else:
        print(f'model_dict[model][\'{model}\'].removeNode()')
        models[model].removeNode()
        del models[model]


def accept_roping():
    global demo_parallel
    global demo_sequence
    r.removeNode()
    rope_look.removeNode()
    np.removeNode()
    for tn in text_nodes:
        tn.removeNode()

    # if demo_parallel.getT() == 0:
    #     for key in models.keys():
    #         models[key].hide()

    # if demo_parallel.isPlaying():
    #     demo_parallel.pause()
    #     print('demo_parallel.pause()')
    #     base.render.ls()
    # else:
    #     demo_parallel.resume()
    #     print('demo_parallel.resume()')

    if demo_sequence.isPlaying():
        demo_sequence.pause()
        if DEVEL:
            print('demo_sequence.pause()')
            base.render.ls()
            print(f'base.camLens.getFov(): {base.camLens.getFov()}')
    else:
        demo_sequence.resume()
        if DEVEL:
            print('demo_sequence.resume()')


# noinspection PyArgumentList
def accept_shift(time):
    # global demo_parallel
    demo_parallel.setT(demo_parallel.getT()+time)
    # demo_parallel.set_t(time)
    # pass

def accept_water():
    r.removeNode()
    rope_look.removeNode()
    models['room_1'].reparent_to(base.render)
    models['room_2'].reparent_to(base.render)
    models['room_3'].reparent_to(base.render)
    # print(models['room_1'].getTightBounds())
    # water_parallel = Parallel()
    water_sequence = Sequence()
    water_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(7.5, 3.5, 0),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    water_sequence.append(ParticleInterval(
        particleEffect=init_water_particle_effect(current_modes_and_filters['render_mode_thickness']),
        parent=base.render,
        worldRelative=True,
        duration=16,
        softStopT=8,
        cleanup=True,
        name='water'
    ))
    # splash_interval = ParticleInterval(
    #     particleEffect=init_splash_particle_effect(current_modes_and_filters['render_mode_thickness']),
    #     parent=base.render,
    #     worldRelative=True,
    #     duration=1,
    #     cleanup=True,
    #     name='splash'
    # )
    water_sequence.start()
    # splash_interval.start()


def start_glow():
    r.removeNode()
    rope_look.removeNode()
    models['room_1'].reparent_to(base.render)
    models['room_2'].reparent_to(base.render)
    models['room_3'].reparent_to(base.render)
    # print(models['room_1'].getTightBounds())
    glow_sequence = Sequence()
    glow_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(7.5, 3.5, 0),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    glow_sequence.append(ParticleInterval(
        particleEffect=init_glow_particle_effect(current_modes_and_filters['render_mode_thickness']),
        parent=base.render,
        worldRelative=True,
        duration=16,
        softStopT=8,
        cleanup=True,
        name='glow'
    ))
    glow_sequence.start()


def start_display(display_particle_effect):
    display_particle_effect.start(parent=base.render)


def soft_stop_display(display_particle_effect):
    display_particle_effect.soft_stop()


def force_display(display_particle_effect):
    # display_particle_effect.removeAllForces()
    display_particle_effect.soft_stop()
    force_group = ForceGroup('zoom')
    a = Randomizer().randomRealUnit()*.1
    # print(a)
    force_group.addForce(LinearNoiseForce(a, 0))  # 0.1500*2
    display_particle_effect.addForceGroup(force_group)


def zoom_function(t):
    fov_min = 20  # 66
    fov_max = 115  # 115
    fov = (fov_min-fov_max)*t+fov_max
    # width = 7.5+t*2.5
    width = 4
    base.camLens.setFov(fov)
    distance = 3.5-width/(2*tan(0.5*fov*2*pi/360))  # 3.5
    # orig_x = spectator.get_x()
    # spectator.set_x(distance)
    spectator.set_x(spectator.getX()+distance-2.225859478385013)
    near = .1-(distance-0.4)
    if near < .1:
        near = .1
    base.camLens.setNear(near)
    # print(width, fov, orig_x, distance, near)
    # print(width, fov, distance, near)


def fov_function(t):
    fov_min = 66  # 66
    fov_max = 115  # 115
    fov = (fov_min-fov_max)*t+fov_max
    base.camLens.setFov(fov)
    # print(fov)


def init_display_sequence():
    r.removeNode()
    rope_look.removeNode()
    display_sequence.start()


def dissolve(t, cube_object):
    cube_object.removeAllForces()
    force_group = ForceGroup()
    force_group.addForce(LinearJitterForce(t*25, 0))
    cube_object.addForceGroup(force_group)
    cube_object.setAlphaScale(1-t)


def start_zoom():
    r.removeNode()
    rope_look.removeNode()
    models['bar'].reparent_to(base.render)
    # fov_min = 66
    # fov_max = 115
    # spectator.setPos(7.5, 3.5, 0)
    # spectator.setHpr(90, 0, 0)
    spectator.set_pos_hpr(-0.3, -1.2, .4, -90, 0, 0)
    # zoom_prepare_parallel = Parallel()
    # zoom_prepare_parallel.append(LerpFunc(fov_function, fromData=0, toData=1, duration=2, blendType='easeInOut'))
    # zoom_prepare_parallel.append(init_pos_interval((1.0-5/(2*tan(0.5*66*2*pi/360)), 0, 0), duration=2))
    # zoom_prepare_parallel.append(LerpPosHprInterval(
    #     nodePath=spectator,
    #     pos=(7.5, 3.5, 0),
    #     hpr=(90, 0, 0),
    #     duration=2,
    #     blendType='easeInOut',
    # ))
    # zoom_sequence.append(zoom_prepare_parallel)

    zoom_sequence.start()


def accept_cubes():
    r.removeNode()
    rope_look.removeNode()
    # models['room_1'].reparent_to(base.render)
    cube_parallels[1].start()


def set_fog_exp_density(t, fog):
    fog.setExpDensity(t)


def set_background_color(t, color, set_preset):
    base.set_background_color(color[0]*t, color[1]*t, color[2]*t)
    set_modes_and_filters(PRESETS[0])
    set_modes_and_filters(PRESETS[set_preset])


def trainspotting_lerp_function(t):
    # base.cam.set_scale(1, 1-(t*.99), 1)
    base.cam.set_scale(1, 1-(t*.9), 1)


def accept_trainspotting():
    r.removeNode()
    rope_look.removeNode()
    # models['room_1'].reparent_to(base.render)
    # models['room_2'].reparent_to(base.render)
    # models['room_3'].reparent_to(base.render)
    models['wc'].reparent_to(base.render)
    trainspotting_sequence.start()


def handshaking_lerp_function(t):
    i = int(len(pos_shake)*t*SHAKE_DEN)-1
    if i < 0:
        i = 0
    base.cam.set_pos(pos_shake[i])
    # print(i, pos_shake[i])
    j = int(len(hpr_shake)*t*SHAKE_DEN)-1
    if j < 0:
        j = 0
    base.cam.set_hpr(hpr_shake[j])


def accept_handshaking():
    r.removeNode()
    rope_look.removeNode()
    np.removeNode()
    for tn in text_nodes:
        tn.removeNode()
    handshaking_sequence.start()


def dust_storm():
    global current_modes_and_filters
    set_preset = current_modes_and_filters['preset']
    # print(set_preset, type(set_preset))
    dust_color = (184/255, 151/255, 122/255)
    # base.set_background_color(*dust_color)
    fog = Fog("Fog")
    fog.set_color(*dust_color)
    fog.setExpDensity(.0)
    base.render.set_fog(fog)
    dust_storm_sequence = Sequence()
    dust_storm_sequence.append(init_pos_interval((-2.89104, 0, 0), duration=2))
    dust_storm_sequence.append(LerpFunctionInterval(
        set_background_color,
        fromData=0,
        toData=1,
        duration=2,
        extraArgs=[dust_color, set_preset]
    ))
    dust_storm_sequence.append(LerpFunctionInterval(
        set_fog_exp_density,
        fromData=0,
        toData=1,
        duration=2,
        extraArgs=[fog]
    ))
    dust_storm_sequence.start()


def init_function():
    # global bar
    pass


def lens_function(t):
    base.camLens.setFov(t)


def accept_effect():
    print('accept_effect()')
    r.removeNode()
    rope_look.removeNode()
    np.removeNode()
    for tn in text_nodes:
        tn.removeNode()
    # models['sign'].reparent_to(base.render)
    # print(models['sign'].getTightBounds())
    # models['garden'].reparent_to(base.render)
    # print(models['garden'].getTightBounds())
    # models['garden_large'].reparent_to(base.render)
    # print(models['garden_large'].getTightBounds())
    # models['podium'].reparent_to(base.render)
    # print(models['podium'].getTightBounds())
    # models['entrance'].reparent_to(base.render)
    # print(models['entrance'].getTightBounds())
    # models['room_1'].reparent_to(base.render)
    # print('room_1:', models['room_1'].getTightBounds())
    # models['room_2'].reparent_to(base.render)
    # print('room_2:', models['room_2'].getTightBounds())
    # models['room_3'].reparent_to(base.render)
    # print('room_3:', models['room_3'].getTightBounds())
    # models['bar'].reparent_to(base.render)
    # print('bar:', models['bar'].getTightBounds())
    # models['hall_low'].reparent_to(base.render)
    # print('hall_low:', models['hall_low'].getTightBounds())
    # models['stairs_low'].reparent_to(base.render)
    # print('stairs_low:', models['stairs_low'].getTightBounds())
    # models['stairs_hi'].reparent_to(base.render)
    # print('stairs_hi:', models['stairs_hi'].getTightBounds())
    models['register'].show()
    # print('register:', models['register'].getTightBounds())
    # models['compo'].reparent_to(base.render)
    # print('compo:', models['compo'].getTightBounds())
    # models['wc'].reparent_to(base.render)
    # print('wc:', models['wc'].getTightBounds())
    # spectator.set_pos_hpr(2.225859478385013, -1.2, .4, -90, 0, 0)
    # base.camLens.setFov(115)
    # interval = ParticleInterval(
    #     particleEffect=init_water_particle_effect(PRESETS[1]['render_mode_thickness']),
    #     parent=base.render,
    #     worldRelative=True,
    #     duration=13,
    #     softStopT=-1.4,  # 11.8
    #     # cleanup=True
    # )
    # interval = ParticleInterval(
    #     particleEffect=init_glow_particle_effect(PRESETS[1]['render_mode_thickness']),
    #     parent=base.render,
    #     worldRelative=True,
    #     duration=16,
    #     softStopT=8,
    #     # cleanup=True,
    #     name='glow'
    # )
    # interval = LerpScaleInterval(spectator, 2, 1, 10, blendType='easeOut')
    # interval = LerpFunc(lens_function, 2, 1, 90, blendType='easeOut')
    # set_modes_and_filters(PRESETS[2])
    # dust_interval.start()
    # greetings_interval.start()
    # set_modes_and_filters(PRESETS[7])
    # base.camLens.setFov(115)
    # spectator.set_pos_hpr(-4.75, -4.95, 0.10, 180, 0, 0)

    # wc_splash_interval.start()

    # set_modes_and_filters(PRESETS[1])
    # rain_splash_parent = base.render.attachNewNode('rain_splash_parent')
    # rain_splash_parent.reparentTo(base.render)
    # rain_splash_parent.setPos(0, 10, 0)
    # rain_splash_interval = ParticleInterval(
    #     particleEffect=init_splash_particle_effect(
    #         point_size=current_modes_and_filters['render_mode_thickness'],
    #         pool_size=round(400),
    #     ),
    #     parent=rain_splash_parent,
    #     worldRelative=False,
    #     duration=0.5+1/60,
    #     softStopT=1/60,
    #     cleanup=True,
    #     name='rain_splash'
    # )
    # rain_splash_interval.start()

    # spectator.set_pos_hpr(-5.5, -4.25, -.7, 90, 0, 0)

    spectator.setPosHpr(-5, -4, 0, 90, 0, 0)
    ring_intervals[0].start()


def display_cleanup():
    for display_particle_effect in display_particle_effects:
        display_particle_effect.cleanup()


def stamp(msg):
    if DEVEL:
        print(f'{round(time.time()-START, 1)}s {msg}')


def retro(retro_key, from_frame, to_frame):
    retro_card[retro_key].find('**/+SequenceNode').node().play(from_frame, to_frame)
    retro_card[retro_key].reparent_to(base.render2d)


def ball_func():
    ball_capture.find('**/+SequenceNode').node().play(0, 215)
    ball_capture.reparent_to(base.render)


def retro_load(retro_key):
    if DEVEL:
        print(f'Loading {retro_key}')
    retro_card[retro_key] = base.loader.loadModel(f'models/{retro_key[:-3]}bam')
    retro_card[retro_key].set_scale(1920/800)


# def bar_value(value):
#     bar['value'] = value
#     base.taskMgr.step(), base.taskMgr.step()


def init_task(task):
    print('init_task')
    # Add some text
    # bk_text = "This is my Demo"
    # textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
    #                           fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
    #                           mayChange=1)
    # print('before sleep')
    # time.sleep(3)
    # if task.time < 3.0:
    #     return Task.cont
    # print('after sleep')
    # textObject.destroy()
    # print('after destroy')


def argasek(t):
    if Randomizer().randomReal(1) < t:
        models['argasek'].show()
        # models['argasek'].set_color_scale(1, 1, 1, 1)
    else:
        models['argasek'].hide()
        # models['argasek'].set_color_scale(1, 1, 1, .15)

#
#     print('pre interval start')
#     init_interval = Func(init_function)
#     init_sequence = Sequence()
#     init_sequence.append(Wait(2/60))
#     # init_sequence.append(Wait(5))
#     init_sequence.append(init_interval)
#     init_sequence.append(Wait(20))
#     init_sequence.append(init_interval)
#     # init_sequence.append(init_interval)
#     init_sequence.start()
#     init_function()
#     print('post interval start')
#
#     # textObject.setText(bk_text)
#
    return Task.done

# Start stamp
stamp('Start loading')

# Config
stamp('Config')
if DEVEL:
    print('sys.platform:', sys.platform)
loadPrcFile("config/Confauto.prc")
loadPrcFile("config/Config.prc")

# Init ShowBase
stamp('Init ShowBase')
base = ShowBase()
# base.taskMgr.step(), base.taskMgr.step()

# noinspection PyUnresolvedReferences
# Print cpMgr, platform, base.win.gsg, etc.
stamp('Print cpMgr, platform, base.win.gsg, etc.')
if DEVEL:
    print(ConfigPageManager.getGlobalPtr())
    print('platform.python_version:', platform.python_version())
    print('platform.machine:', platform.machine())
    print('base.win.gsg.driver_vendor:', base.win.gsg.driver_vendor)
    print('base.win.gsg.driver_renderer:', base.win.gsg.driver_renderer)
    print('base.win.gsg.supports_basic_shaders:', base.win.gsg.supports_basic_shaders)
    print("PandaSystem.version_string:", PandaSystem.version_string)

# Set window & background color
stamp('Set window & background color')
fullscreen = False
props = WindowProperties()
props.setIconFilename('icons/icon-256.png')
props.setTitle('Kramsta by Damage')
if not DEVEL:
    props.setCursorHidden(True)
base.win.request_properties(props)
base.setBackgroundColor(0, 0, 0)
toggle_fullscreen()

# Load Dekramsting
stamp('Load Dekramsting')
set_cm = {}
set_card = {}
set_tex = {}
for i in range(14, 24+1):
    if DEVEL:
        print(f'models/set_{i}_fit.png')
    set_cm[i] = CardMaker(f'Dekramsting {i}')
    set_cm[i].setFrameFullscreenQuad()
    set_card[i] = base.render2d.attachNewNode(set_cm[i].generate())
    set_tex[i] = base.loader.loadTexture(f'models/set_{i}_fit.png')
    set_card[i].setTexture(set_tex[i])
    set_card[i].setTransparency(TransparencyAttrib.M_alpha)
    set_card[i].hide()


# Init direct wait bar
set_card[14].show()
# bar = DirectWaitBar(text='Dekramsting...')
# bar['barBorderWidth'] = (10, 10)
# bar.setBarRelief(0)
base.taskMgr.step(), base.taskMgr.step(), base.taskMgr.step(), base.taskMgr.step()

# Set camera lens field of view
stamp('Set camera lens field of view')
base.camLens.setFov(90)
base.camLens.setNear(.1)

# base.camLens.setAspectRatio(1920/1080)
# print(f'base.camLens.getAspectRatio(): {base.camLens.getAspectRatio()}')

# Set frame rate meter
stamp('Set frame rate meter')
if DEVEL:
    base.set_frame_rate_meter(True)

# Setting fullscreen
# props = WindowProperties()
# props.set_fullscreen(True)
# base.win.request_properties(props)

# Setting fullscreen with correct size
# props = WindowProperties()
# props.set_size(base.pipe.get_display_width(), base.pipe.get_display_height())
# props.set_fullscreen(True)
# base.win.request_properties(props)

# props.setCursorHidden(True)

# "Fullscreen" with upper bar and bottom dock
# props = WindowProperties()
# props.set_size(base.pipe.get_display_width(), base.pipe.get_display_height())
# props.setOrigin((0, 0))
# base.win.request_properties(props)

# props.set_size(1920, 1080)
# props.set_size(1280, 720)
# props.setFixedSize(True)
# props.set_size(1280, 720)
# props.set_size(1920, 1080)
# props.set_size(2560, 1600)
# print(base.pipe.get_display_width(), base.pipe.get_display_height())
# props.set_size(base.pipe.get_display_width(), base.pipe.get_display_height())
# props.setOrigin((-2, -2))
# props.setOrigin((0, 0))
# props.set_fullscreen(True)
# base.win.request_properties(props)

# Set currents, lasts, deltas and weights
currents = [0, 0, 0, 0, 0, 0, 1, base.camLens.getFov()[0]]
lasts = [0, 0, 0, 0, 0, 0, 1, base.camLens.getFov()[0]]
deltas = [0, 0, 0, 0, 0, 0, 0, 0]
weights = [1, 1, 1, .2, .2, .2, 50, .1]
# delta = 0

# Set period
period = 120/125

# def get_pos_interval():
#     pass

# Set spectator
spectator = base.render.attach_new_node('spectator')
spectator.reparent_to(base.render)
base.camera.reparent_to(spectator)
# spectator.set_y(-2)

# spectator.set_pos_hpr(0, 0, 0, 0, 0, 0)

# spectator.set_pos_hpr(0, 0, 0, -110, 0, 0)
# spectator.set_pos_hpr(0, -.8, 0, 0, 0, 0)

path = sys.path[0]
if path.endswith('Contents/MacOS/../Frameworks'):
    path = str(pathlib.Path().absolute())
if DEVEL:
    print('path:', path)

# Download
stamp('Download')
if DEVEL:
    # noinspection PyUnresolvedReferences
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print('Downloading camera.csv')
    # url = 'http'+'://camera.leszcz.uk'
    url = 'https://docs.google.com/spreadsheets/d/14FrIBHotjeTTjMmCdHFe7VlGDkBHL83Vpx5ArMxZL8k/export?format=csv&id=14FrIBHotjeTTjMmCdHFe7VlGDkBHL83Vpx5ArMxZL8k'
    r = requests.get(url, allow_redirects=True, verify=False)
    open(path+'/models/camera.csv', 'wb').write(r.content)
    print('Downloading events.tsv')
    # url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQOuBd20jiDYamDCsvKyWJgqer1KWPbpylgGYppawi4XOQ5eOQOYvJjr4db3CwnnQ3uOzhWPGdGMPcn/pub?gid=0&single=true&output=tsv'
    url = 'https://docs.google.com/spreadsheets/d/13dFTwxkqh0AiPdm_jZd1tMuqR0y-uJxUz0cbWgAUcp0/export?format=tsv&id=13dFTwxkqh0AiPdm_jZd1tMuqR0y-uJxUz0cbWgAUcp0'
    r = requests.get(url, allow_redirects=True, verify=False)
    open(path+'/models/events.tsv', 'wb').write(r.content)

# Rope
steps = 7
stamp('Rope')
look_color = (1, .5, 1, 1)
demo_parallel = Parallel()
demo_sequence = Sequence(
    # Func(retro_load, 'retro_td.mkv'), Func(bar_value, 1/steps),
    # Func(retro_load, 'retro_rw.mkv'), Func(bar_value, 2/steps),
    # Func(retro_load, 'retro_sf.mkv'), Func(bar_value, 3/steps),
    # Func(retro_load, 'retro_v1b.mkv'), Func(bar_value, 4/steps),
    # Func(retro_load, 'retro_v2.mkv'), Func(bar_value, 5/steps),
    # Func(retro_load, 'retro_v1.mkv'), Func(bar_value, 6/steps),
    # Func(time.sleep, 1), Func(bar_value, 1/steps*100),
    # Func(time.sleep, 1), Func(bar_value, 2/steps*100),
    # Func(time.sleep, 1), Func(bar_value, 3/steps*100),
    # Wait(1), Func(bar_value, 4/steps*100),
    # Wait(1), Func(bar_value, 5/steps*100),
    # Wait(1), Func(bar_value, 50),
    # Wait(1), Func(bar_value, 100),
    # Func(bar.destroy),
    Wait(2),
    demo_parallel,
)
roping_sequence = Sequence()
with open(path+'/models/camera.csv') as file_object:
    csv_lines = file_object.readlines()
vertices = []
look_vertices = []
lines = LineSegs()
lines.setColor(1, 0, 1)
text_nodes = []
for csv_line in csv_lines[1+0:]:
    cols = csv_line.split(',')
    if DEVEL:
        text = TextNode(cols[2])
        text.setText(cols[2])
        text_nodes.append(base.render.attachNewNode(text))
        text_nodes[-1].setP(-90)
        text_nodes[-1].setPos(float(cols[3]), float(cols[4]), float(cols[5]))
        text_nodes[-1].setScale(.5)
        text_nodes[-1].reparentTo(base.render)
    vertices.append((None, (float(cols[3]), float(cols[4]), float(cols[5]))))
    look_vertices.append({'point': (float(cols[6]), float(cols[7]), float(cols[8])), 'color': look_color})
    lines.moveTo(float(cols[3]), float(cols[4]), float(cols[5]))
    lines.drawTo(float(cols[6]), float(cols[7]), float(cols[8]))
node = lines.create()
np = NodePath(node)
r = Rope()
r.setup(4, vertices)
r.ropeNode.setThickness(2)
r.ropeNode.setNumSubdiv(1 * 120)
r.setPos(0, 0, 0)
if DEVEL:
    np.reparentTo(base.render)
    r.reparentTo(base.render)
r.recompute()
rope_look = Rope()
rope_look.setup(4, look_vertices)
rope_look.ropeNode.setUseVertexColor(1)
rope_look.ropeNode.setThickness(2)
rope_look.ropeNode.setNumSubdiv(1 * 120)
rope_look.setPos(0, 0, 0)
rope_look.recompute()
roping_sequence.append(LerpFunc(
    function=roping_function,
    fromData=0,
    toData=1,
    duration=len(vertices) * 1,
    # extraArgs=[points, looks],
))
# demo_parallel.append(models_sequence)
demo_parallel.append(roping_sequence)

# points = r.getPoints(5 * 120 * 100)

# Append position intervals
stamp('Append position intervals')
dummy = base.render.attachNewNode("dummy")
sequence = Sequence()
rn = Randomizer()
old_hpr = spectator.getHpr()
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
    interval = LerpPosHprInterval(nodePath=spectator,
                                  duration=period*4,
                                  pos=pos1,
                                  hpr=new_hpr,
                                  blendType='easeOut')  # period
    sequence.append(interval)


# Append beat intervals
stamp('Append beat intervals')
beat_interval = LerpFunc(beat, fromData=0, toData=1, duration=period/4)
beat_count = 0

pos_intervals = False

# Load models, make point-clouds and hide models
stamp('Load models, make point-clouds and hide models')
model_dict = {
    'alco': {'name': 'alco', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'spodek': {'name': 'spodek', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_0': {'name': 'villa_0', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_1': {'name': 'villa_1', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_garden': {'name': 'villa_garden', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_street': {'name': 'villa_street', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'nox': {'name': 'nox', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'xenium': {'name': 'xenium', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'river': {'name': 'river', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'signboard': {'name': 'signboard', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_2': {'name': 'villa_2', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_3': {'name': 'villa_3', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'villa_4': {'name': 'villa_4', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'protracker': {'name': 'protracker', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'p1': {'name': 'p1', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'p2': {'name': 'p2', 'pos_hpr': (0, 1, 0, 0, 0, 0)},
    'p3': {'name': 'p3', 'pos_hpr': (0, 1, 0, 0, 0, 0)},

    'argasek': {'name': 'argasek', 'pos_hpr': (4.6, -0.95, 0.15, -90, 0, 0)},
    'ball': {'name': 'ball', 'pos_hpr': (2.7, -0.25, 0-.75/2, 90, -60, 0)},

    'sign': {'name': 'sign', 'pos_hpr': (17.5, 9.4, 2.8, 0, 0, 0)},
    'garden': {'name': 'garden_5', 'pos_hpr': (22.1, 0.5, .5, 0, 0, 0)},
    'garden_large': {'name': 'garden_large_10', 'pos_hpr': (18, -10.7, .5, 0, 0, 0)},
    'podium': {'name': 'podium_3', 'pos_hpr': (15.5, -2.8, 2.7, 175.5, 0, 0)},
    'entrance': {'name': 'entrance_3', 'pos_hpr': (12.0, 4.8, 1.8, 83, 0, 0)},  # -109
    'room_1': {'name': 'room_1', 'pos_hpr': (+5.7, 3.5, 0, +147, 0, 0)},
    'room_2': {'name': 'room_2', 'pos_hpr': (-1, 3, 0, +132, 90, 0)},
    'room_3': {'name': 'room_3', 'pos_hpr': (-5.3, 4.15, -.1, +92, 0, 0)},
    'bar': {'name': 'bar', 'pos_hpr': (1.9, -3.4, 0, 56, 0, 0)},
    'hall_low': {'name': 'hall_low', 'pos_hpr': (-4.1, -2.0, 1.5, 0, 0, 0)},
    'wc': {'name': 'wc', 'pos_hpr': (-4.0, -3.7, 0, 90, 0, 0)},
    'stairs_low': {'name': 'stairs_low', 'pos_hpr': (-4.1, -2.0, 1.5, 0, 0, 0)},
    'stairs_hi': {'name': 'stairs_hi', 'pos_hpr': (-4.1, -2.0, 1.5, 0, 0, 0)},
    'register': {'name': 'register_half', 'pos_hpr': (-4.1, -2.0, 1.5, 0, 0, 0)},
    'compo': {'name': 'compo_200k', 'pos_hpr': (5.6, -4.0, 1.1, -109.5, 0, 0)},

    'background': {'name': 'background', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '0': {'name': '0', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '1': {'name': '1', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '2': {'name': '2', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '3': {'name': '3', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '4': {'name': '4', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '5': {'name': '5', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    '6': {'name': '6', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
}
models = {}
for model_key in model_dict:
    # print(model_key, model_dict[model_key])
    name = model_dict[model_key]['name']
    models[model_key] = base.loader.loadModel(f'models/{name}.bam')
    models[model_key].set_pos_hpr(*model_dict[model_key]['pos_hpr'])
    models[model_key].reparentTo(base.render)
    models[model_key].hide()
models['compo'].setTransparency(TransparencyAttrib.M_alpha)
models['argasek'].setTransparency(TransparencyAttrib.M_alpha)
models['argasek'].setColorScale(1, 1, 1, 0)
models['ball'].setTransparency(TransparencyAttrib.M_alpha)
models['ball'].setScale(.75)
models['background'].show()
models['0'].show()
models['1'].show()
models['2'].show()
models['3'].show()
models['4'].show()
models['5'].show()
models['6'].show()
clock = base.render.attach_new_node('clock')
models['background'].reparent_to(clock)
models['0'].reparent_to(clock)
models['1'].reparent_to(clock)
models['2'].reparent_to(clock)
models['3'].reparent_to(clock)
models['4'].reparent_to(clock)
models['5'].reparent_to(clock)
models['6'].reparent_to(clock)
# models['0'].setPos(0, -1, 0)
# models['1'].setPos(0, -1, 0)
# models['2'].setPos(0, -1, 0)
# models['3'].setPos(0, -1, 0)
# models['4'].setPos(0, -1, 0)
# models['5'].setPos(0, -1, 0)
# models['6'].setPos(0, -1, 0)
clock.set_scale(1.5)
# print(clock.getTightBounds())
# exit()
clock.set_pos_hpr(5.1, -4.0, 3.1, 0, 0, 0)
clock.hide()
clock_intervals = []
for indicator in range(0, 6+1):
    clock_intervals.append(Sequence())
    indicator_duration = 2**indicator/8
    indicator_steps = 2**(6-indicator)*2
    indicator_sign = 1 if indicator % 2 == 0 else -1
    # if DEVEL:
    #     print(f'indicator = {indicator}')
    #     print(f'indicator_duration = {indicator_duration}')
    #     print(f'indicator_steps = {indicator_steps}')
    #     print(f'indicator_sign = {indicator_sign}')
    for angle in range(1*30, (indicator_steps+1)*30, 30):
        # if DEVEL:
        #     print(angle)
        clock_intervals[indicator].append(
            LerpHprInterval(
                nodePath=models[f'{indicator}'],
                duration=indicator_duration,
                hpr=(0, 0, angle*indicator_sign),
                blendType='easeIn',
            )
        )
    # if DEVEL:
    #     print(clock_intervals[indicator])
clock_interval = Parallel(
    clock_intervals[0],
    clock_intervals[1],
    clock_intervals[2],
    clock_intervals[3],
    clock_intervals[4],
    clock_intervals[5],
    clock_intervals[6],
)
# if DEVEL:
#     print(clock_interval)
# exit()

# models['argasek'].show()

# bar['value'] += 10
set_card[14].remove_node()
set_card[15].show()
base.taskMgr.step(), base.taskMgr.step()

# Render modes and common filters
stamp('Render modes and common filters')
filters = CommonFilters(base.win, base.cam)
for preset in (PRESETS[8], PRESETS[7], PRESETS[6], PRESETS[3], PRESETS[2], PRESETS[1], PRESETS[0]):
    set_modes_and_filters(preset)
# for preset in PRESETS[::-1]:
#     set_modes_and_filters(preset)

# Get points and looks
stamp('Get points and looks')
points = r.getPoints(len(vertices) * 5000)
looks = rope_look.getPoints(len(vertices) * 5000)
# bar['value'] += 10
set_card[15].remove_node()
set_card[16].show()
base.taskMgr.step(), base.taskMgr.step()
# jumps = (
#     (4 * 60 + 22.28) * 5000,
#     (4 * 60 + 22.38) * 5000,
#     (4 * 60 + 22.47) * 5000,
#     (4 * 60 + 22.56) * 5000,
#     (4 * 60 + 22.66) * 5000,
#     (4 * 60 + 23.00) * 5000,
#     (4 * 60 + 23.09) * 5000,
#     (4 * 60 + 23.19) * 5000,
#     (4 * 60 + 23.28) * 5000,
#     (4 * 60 + 23.38) * 5000,
#     (4 * 60 + 23.47) * 5000,
#     (4 * 60 + 23.56) * 5000,
#     (4 * 60 + 23.66) * 5000,
#     (4 * 60 + 24.00) * 5000,
# )
# for jump_i in range(len(jumps)-1):
#     jump_to = points[int(jumps[jump_i+1])]
#     print(jump_to)
#     for points_i in range(int(jumps[jump_i]), int(jumps[jump_i+1])):
#         points[points_i] = jump_to

# Set spectator pos & hpr
stamp('Set spectator pos & hpr')

# print(len(looks))
# spectator.set_pos(points[0])
# spectator.lookAt(looks[0])
spectator.set_pos_hpr(0, 0, 10, 0, -90, 0)
# spectator.set_pos_hpr(0, 0, 0, 90, 0, 0)
# spectator.set_pos_hpr(18.5, 9.6, 2.8, 0, -90, 0)
# spectator.set_pos_hpr(18.5, 9.6, 2.8, 90, 0, 0)
# models['sign'].reparent_to(base.render)
# models['garden'].reparent_to(base.render)
models['garden_large'].show()
# models['podium'].reparent_to(base.render)
# models['entrance'].reparent_to(base.render)
# models['room_1'].reparent_to(base.render)
# models['room_2'].reparent_to(base.render)
# models['room_3'].reparent_to(base.render)
# models['bar'].reparent_to(base.render)
# models['hall_low'].reparent_to(base.render)
# models['stairs_low'].reparent_to(base.render)
# models['wc'].reparent_to(base.render)
# models['register'].reparent_to(base.render)
# models['compo'].reparent_to(base.render)

# Enable particles
stamp('Enable particles')
base.enableParticles()

# Subtitles
stamp('Subtitles')
texts = (
    'Polish Scene Chronicle',  # 0
    'The von Kramsta family villa',  # 1
    'a villa with a garden',  # 2
    'built in the third quarter of the 19th century',  # 3
    'in the center of Katowice,',  # 4
    'at ul. Warszawska 37,',  # 5
    'it is entered',  # 6
    'In the 1950s,',  # 7
    'from the side of ul. Warszawska',  # 8
    'For several years',  # 9
    'They self-proclaimed themselves as Demoscene.',  # 10
    'Apart from consuming huge amounts of alcoholic beverages,',  # 11
    'these party goers',  # 12
    'watch some daubs, and some demos.',  # 13
    '',  # 14
    'The party is called \"Xenium\",',  # 15
    '\"Your Mother Washes in the River\".',  # 16
    'That sad guy at the bar is Argasek ^ BrCr',  # 17
    'the worst TOILET in Scotland',  # 18
    'GLORY TO SCIENCE',  # 19
    'in the register of immovable monuments of the Silesia Voivodeship.',  # 20
    '',  # 21
    'the facility was allocated to the Creative Work Club.',  # 22
    'In these',  # 23
    'was occupied by the editorial staff of the ephemeral',  # 24
    'rallies of computer enthusiasts have been held here.',  # 25
    'listen to strange music,',  # 26
    'and earlier in free translation,',  # 27
)
subtitles = []
for text in texts:
    subtitles.append(
        OnscreenText(text=text,  # text
            pos=(0, -.95),  # +.96
            fg=(1, 1, 1, 1),
            bg=(0, 0, 0, .5),
            scale=0.06,  # 40%
            align=TextNode.ACenter,
        )
    )
for subtitle in subtitles:
    subtitle.hide()

# Init display_sequence
stamp('Init display_sequence')
my_image_path = 'models/lead_new_48x27.png'
if path.startswith('/'):
    my_image_path = path+'/'+my_image_path
if DEVEL:
    print('my_image_path:', my_image_path)
my_image = PNMImage(my_image_path)  # Read image (opt: 64x36)
display_sequence = Sequence()  # Initialise sequence
display_particle_effects = []  # Append particle effects
tile_size = 1.920 / my_image.getXSize()
for x in range(my_image.getXSize()):
    for z in range(my_image.getYSize()):
        min_x = (x - (my_image.getXSize() / 2)) * tile_size
        min_z = -(z - (my_image.getYSize() / 2)) * tile_size
        max_x = ((x + 1) - (my_image.getXSize() / 2)) * tile_size
        max_z = -((z + 1) - (my_image.getYSize() / 2)) * tile_size
        xel_a = my_image.getXelA(x, z)
        # print(xel_a)
        if xel_a[3] > 0.5:  # 0.5 0.6 0.4 0.35
            xel_a[3] = 1
            display_particle_effects.append(init_display_particle_effect(
                # current_modes_and_filters['render_mode_thickness'],
                PRESETS[1]['render_mode_thickness'],
                min_x,
                min_z,
                max_x,
                max_z,
                xel_a
            ))
if DEVEL:
    print('len(display_particle_effects):', len(display_particle_effects))
    # exit()
for display_particle_effect in display_particle_effects:  # Append functions
    display_sequence.append(Func(start_display, display_particle_effect))
display_sequence.append(Wait(5))  # Append wait
for display_particle_effect in display_particle_effects:  # Append particle outs
    display_sequence.append(Func(force_display, display_particle_effect))

# Sound interval
stamp('Sound interval')
music = base.loader.loadSfx("audio/Kramsta.ogg")  # Load music
demo_parallel.append(
    SoundInterval(
        music,
        loop=0,
        volume=1,
        startTime=0,
    )
)

# Rain interval
stamp('Rain interval')
rain_interval = ParticleInterval(
    particleEffect=init_water_particle_effect(PRESETS[1]['render_mode_thickness']),
    parent=base.render,
    worldRelative=True,
    duration=13,
    softStopT=-1.4,  # 11.8
    # cleanup=True,
    name='rain'
)

# Glow interval
stamp('Glow interval')
glow_interval = ParticleInterval(
    particleEffect=init_glow_particle_effect(PRESETS[1]['render_mode_thickness']),
    parent=base.render,
    worldRelative=True,
    duration=9,
    softStopT=-1.1,
    cleanup=True,
    name='glow'
)

# Zoom sequence and dust intervals
stamp('Zoom sequence and dust intervals')
zoom_sequence = Sequence()
zoom_sequence.append(LerpFunc(zoom_function, fromData=0, toData=1, duration=4, blendType='easeInOut'))
zoom_sequence.append(LerpFunc(zoom_function, fromData=1, toData=0, duration=4, blendType='easeInOut'))
dust_parent = base.render.attachNewNode("dust parent")
dust_parent.reparentTo(base.render)
dust_parent.setPos(-0.3, -1.2, -.55)  # dust start pos
# dust_parent.setPos(5.5, -1.6, -.5)  # dust end pos
dust_lerp_pos_interval = LerpPosInterval(
    nodePath=dust_parent,
    duration=8,
    pos=(5.4, -1.6, -.55),
    startPos=(-0.3, -1.2, -.55),
    blendType='easeOut',
)
dust_interval = Parallel(
    ParticleInterval(
        particleEffect=init_dust_particle_effect(PRESETS[2]['render_mode_thickness']),
        parent=dust_parent,
        worldRelative=False,
        duration=16,
        softStopT=-1,  # 11.8
        cleanup=False,
    ),
    Sequence(
        dust_lerp_pos_interval,
        zoom_sequence,
    )
)
dust_interval_2 = Parallel(
    ParticleInterval(
        particleEffect=init_dust_particle_effect(PRESETS[2]['render_mode_thickness']),
        parent=dust_parent,
        worldRelative=False,
        duration=8,
        softStopT=-1,  # 11.8
        cleanup=False,
    ),
    dust_lerp_pos_interval,
)
dust_interval_3 = Parallel(
    ParticleInterval(
        particleEffect=init_dust_particle_effect(PRESETS[2]['render_mode_thickness']),
        parent=dust_parent,
        worldRelative=False,
        duration=8,
        softStopT=-1,  # 11.8
        cleanup=False,
    ),
    LerpPosInterval(
        nodePath=dust_parent,
        duration=8,
        pos=(-0.3, -1.2, -1.16693),
        startPos=(-2.7, -3.6, -1.16693),
        # blendType='easeOut',
    )
)

# Trainspotting sequence
stamp('Trainspotting sequence')
trainspotting_sequence = Sequence()
trainspotting_sequence.append(LerpFunctionInterval(
    trainspotting_lerp_function,
    fromData=0,
    toData=1,
    duration=2,
    blendType='easeInOut',
))
trainspotting_sequence.append(LerpFunctionInterval(
    trainspotting_lerp_function,
    fromData=1,
    toData=0,
    duration=2,
    blendType='easeInOut',
))

# Boards
stamp('Boards')
MAX_POS = .1/2
MAX_HPR = 5/2
board_intervals = {}
for board_key in (
        'villa_0',
        'villa_garden',
        'spodek',
        'villa_street',
        'villa_1',
        'signboard',
        'villa_2',
        'villa_3',
        'villa_4',
        'p1',
        'p2',
        'p3',
        'alco',
        'protracker',
        'xenium',
        'river',
        'nox',
):
    rn = Randomizer()
    models[board_key].setTransparency(TransparencyAttrib.M_alpha)
    duration = 3.1 # 1.44
    board_interval = Sequence(
        Func(models[board_key].show),
        Parallel(
            LerpColorScaleInterval(
                nodePath=models[board_key],
                duration=duration,
                colorScale=(1, 1, 1, 0),
                # colorScale=(0, 0, 0, 1),
                startColorScale=(1, 1, 1, 1),
                blendType='easeOut'
            ),
            LerpPosHprInterval(
                nodePath=models[board_key],
                duration=duration,
                pos=(
                    rn.randomRealUnit() * 2 * MAX_POS,
                    rn.randomRealUnit() * 2 * MAX_POS + .59,
                    rn.randomRealUnit() * 2 * MAX_POS
                ),
                hpr=(
                    rn.randomRealUnit() * 2 * MAX_HPR,
                    rn.randomRealUnit() * 2 * MAX_HPR,
                    rn.randomRealUnit() * 2 * MAX_HPR
                ),
                startPos=(
                    rn.randomRealUnit() * 2 * MAX_POS,
                    rn.randomRealUnit() * 2 * MAX_POS + .59,
                    rn.randomRealUnit() * 2 * MAX_POS
                ),
                startHpr=(
                    rn.randomRealUnit() * 2 * MAX_HPR,
                    rn.randomRealUnit() * 2 * MAX_HPR,
                    rn.randomRealUnit() * 2 * MAX_HPR
                ),
            ),
        ),
        Func(models[board_key].detachNode),
    )
    board_intervals[board_key] = board_interval

# # Retro demo player
stamp('Retro demo player')
dekramsting_i = 17
for retro_key in (
        'retro_td.mkv',
        'retro_rw.mkv',
        'retro_sf.mkv',
        'retro_v1b.mkv',
        'retro_v2.mkv',
        'retro_v1.mkv'
):
    # retro_card[retro_key] = base.render.attach_new_node(retro_key)
    retro_load(retro_key)
    set_card[dekramsting_i-1].remove_node()
    set_card[dekramsting_i].show()
    dekramsting_i += 1
    # bar['value'] += 10
    base.taskMgr.step(), base.taskMgr.step()

stamp('Loading ball capture')
ball_capture = base.loader.loadModel('models/ball_capture.bam')
ball_capture.set_pos_hpr(19.8, -21.7, 1.80, 180, 0, 0)
ball_capture.set_scale(1.920*2.8, 1, 1.080*2.8)
# print(ball_capture.get_tight_bounds())
# print(models['garden_large'].get_tight_bounds())
# exit()
set_card[22].remove_node()
set_card[23].show()
# bar['value'] += 10
base.taskMgr.step(), base.taskMgr.step()

# Making cards
stamp('Making cards')
# set_cm = {}
# set_card = {}
# set_tex = {}
for i in range(13+1):
    if DEVEL:
        print(f'models/set_{i}_fit.png')
    set_cm[i] = CardMaker(f'Set Rector {i}')
    set_cm[i].setFrameFullscreenQuad()
    set_card[i] = base.render2d.attachNewNode(set_cm[i].generate())
    set_tex[i] = base.loader.loadTexture(f'models/set_{i}_fit.png')
    set_card[i].setTexture(set_tex[i])
    set_card[i].hide()
set_card[6].setTransparency(TransparencyAttrib.M_alpha)
set_card[7].setTransparency(TransparencyAttrib.M_alpha)
set_card[6].setPos(0, 0, 1.3)
# set_card[13].setTransparency(TransparencyAttrib.M_alpha)
# set_card[13].set_color_scale(1, 1, 1, 0)
# bar['value'] += 10
set_card[23].remove_node()
set_card[24].show()
base.taskMgr.step(), base.taskMgr.step()
# set_card[13].show()

# Mirror
stamp('Mirror')
format = GeomVertexFormat.getV3n3c4()
vertexData = GeomVertexData('mirror', format, Geom.UHStatic)
vertexData.setNumRows(4)
vertices = GeomVertexWriter(vertexData, 'vertex')
vertices.addData3f(-1, 0, 1)
vertices.addData3f(1, 0, 1)
vertices.addData3f(1, 0, -1)
vertices.addData3f(-1, 0, -1)
# Store the triangles, counter clockwise from front
primitive = GeomTriangles(Geom.UHStatic)
primitive.addVertices(3, 1, 0)
primitive.addVertices(3, 2, 1)
geom = Geom(vertexData)
geom.addPrimitive(primitive)
node = GeomNode('mirror gnode')
node.addGeom(geom)
mirror_node_path = base.render.attachNewNode(node)
mirror_node_path.hide()
mirror_node_path.setTransparency(TransparencyAttrib.M_alpha)
# tex = base.loader.loadTexture('models/Neon-Square-PNG-Clipart.png')
tex = base.loader.loadTexture('models/greetings.png')
mirror_node_path.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
mirror_node_path.setTexTransform(TextureStage.getDefault(), TransformState.makeHpr(LVecBase3f(0, -90, 0)))
mirror_node_path.setTexOffset(TextureStage.getDefault(), .5, .5)
mirror_node_path.setTexScale(TextureStage.getDefault(), .5, 1, .5)
mirror_node_path.setTexProjector(TextureStage.getDefault(), base.render, mirror_node_path)
mirror_node_path.setTexture(tex)
mirror_node_path.set_pos_hpr(-4.75, -5.25, 0.35, 180, 0, 0)
mirror_node_path.set_scale(0.8)
wc_splash_parent = base.render.attachNewNode('wc_splash_parent')
wc_splash_parent.reparentTo(base.render)
wc_splash_parent.setPos(-6.2, -4.23, -.8)
wc_splash_interval = ParticleInterval(
    particleEffect=init_splash_particle_effect(
        point_size=PRESETS[7]['render_mode_thickness'],
        pool_size=round(400*60*0.5)
    ),
    parent=wc_splash_parent,
    worldRelative=False,
    duration=4,
    softStopT=-.5,
    cleanup=True,
    name='wc_splash'
)
greetings_interval = ParticleInterval(
    particleEffect=init_greetings_particle_effect(PRESETS[7]['render_mode_thickness']),
    parent=base.render,
    worldRelative=True,
    duration=7.44,  # 7.44, 11.44
    # softStopT=-1,
    softStopT=-2.25,  # Greetsy do ko??ca nie wygasaja
    # cleanup=True,
    name='greetings'
)

# Cube
colors = (
    "ff4800",
    "e200d5",
    "305cff",
    "00d062",
    "ff3bca",
    "3bb8ff",
    "5bb800",
    "c20000",
    "dc004e",
    "8c00dc",
    "00aeb4",
    "caff6d",
    "6dd7ff",
    "c66dff",
    "55bd27",
    "7b37aa",
    "ff0000",
    "ffcc00",
    "2b27cc",
    "c66a98",
)
stamp('Cube')
cube_duration = 1.18
rotation = 180
cube_parent_0 = base.render.attachNewNode('cube_parent_0')
cube_parent_1 = base.render.attachNewNode('cube_parent_1')
# cube_parent_0.setPos(-3.25, -4, 3.1)
cube_parent_0.setPos(-3.25, (-7.5+0.5)*1/3-0.5, 3.1)
cube_parent_1.setPos(-3.25, (-7.5+0.5)*2/3-0.5, 3.1)
cube_parallels = []
for cube_number in range(17):
    cube_parallel = Parallel()
    color = colors[cube_number]
    cube = init_cube_particle_effect(
        PRESETS[6]['render_mode_thickness'],
        Randomizer().randomReal(.5)*2 + .5,
        Randomizer().randomReal(.5)*2 + .5,
        Randomizer().randomReal(.5)*2 + .5,
        # kolory do poprawy
        # (Randomizer().randomReal(.5) + .5, Randomizer().randomReal(.5) + .5, Randomizer().randomReal(.5) + .5, 1),
        (int(color[0:2], 16)/255, int(color[2:4], 16)/255, int(color[4:6], 16)/255, 1),
        cube_duration,
    )
    cube_parallel.append(
        LerpFunc(
            function=dissolve,
            fromData=0,
            toData=1,
            duration=cube_duration,
            blendType='easeIn',
            extraArgs=[cube],
        )
    )
    cube_parallel.append(
        ParticleInterval(
            particleEffect=cube,
            parent=(cube_parent_0, cube_parent_1)[cube_number % 2],
            worldRelative=False,
            duration=cube_duration,
            cleanup=True,
        )
    )
    start_h = Randomizer().randomInt(360)
    start_p = Randomizer().randomInt(360)
    start_r = Randomizer().randomInt(360)
    cube_parallel.append(
        LerpHprInterval(
            nodePath=cube,
            duration=cube_duration,
            hpr=(
                start_h + Randomizer().randomRealUnit() * rotation,
                start_p + Randomizer().randomRealUnit() * rotation,
                start_r + Randomizer().randomRealUnit() * rotation,
            ),
            startHpr=(start_h, start_p, start_r),
        )
    )
    cube_parallels.append(cube_parallel)
# exit()

# Rings
ring_intervals = []
ring_parents = []
for ring_i in range(14):
    ring_parents.append(base.render.attachNewNode(f'ring parent {ring_i}'))
    ring_x = (RING_STOP-RING_START)*(ring_i+1)/15+RING_START
    ring_parents[ring_i].setPosHpr(ring_x, -4.0, 3.1, 90, 90, 0)
    ring_intervals.append(
        ParticleInterval(
            particleEffect=init_ring_particle_effect(
                point_size=PRESETS[6]['render_mode_thickness'],
            ),
            parent=ring_parents[ring_i],
            worldRelative=False,
            duration=.30,
            cleanup=False,
            name=f'ring interval {ring_i}',
        )
    )

# Steam interval (middle -3.95)
stamp('Steam interval')
steam_interval = Parallel(
    ParticleInterval(
        particleEffect=init_steam_particle_effect(
            PRESETS[8]['render_mode_thickness'],
            litter_size=int(200*(2.4/7.8)),
            min_bound=(0, -7.9, 1.01067),
            max_bound=(7, -5.5, 1.01067),
        ),
        parent=base.render,
        worldRelative=True,
        duration=16,
        softStopT=-4,
        cleanup=False,
        name='steam right'
    ),
    ParticleInterval(
        particleEffect=init_steam_particle_effect(
            PRESETS[8]['render_mode_thickness'],
            litter_size=int(200*(3.0/7.8)),
            min_bound=(0, -5.5, 1.01067),
            max_bound=(7, -2.5, 1.01067),
        ),
        parent=base.render,
        worldRelative=True,
        duration=6,
        softStopT=-4,
        cleanup=False,
        name='steam center'
    ),
    ParticleInterval(
        particleEffect=init_steam_particle_effect(
            PRESETS[8]['render_mode_thickness'],
            litter_size=int(200*(2.4/7.8)),
            min_bound=(0, -2.5, 1.01067),
            max_bound=(7, -0.1, 1.01067),
        ),
        parent=base.render,
        worldRelative=True,
        duration=16,
        softStopT=-4,
        cleanup=False,
        name='steam left'
    ),
)

# Credits
stamp('Credits')
credits_format = GeomVertexFormat.getV3n3c4()
credits_vertex_data = GeomVertexData('credits', format, Geom.UHStatic)
credits_vertex_data.setNumRows(4)
credits_vertices = GeomVertexWriter(credits_vertex_data, 'vertex')
credits_vertices.addData3f(-1.920, 0, 1.080)
credits_vertices.addData3f(1.920, 0, 1.080)
credits_vertices.addData3f(1.920, 0, -1.080)
credits_vertices.addData3f(-1.920, 0, -1.080)
# Store the triangles, counter clockwise from front
credits_primitive = GeomTriangles(Geom.UHStatic)
credits_primitive.addVertices(3, 1, 0)
credits_primitive.addVertices(3, 2, 1)
credits_geom = Geom(credits_vertex_data)
credits_geom.addPrimitive(credits_primitive)
credits_node = GeomNode('credits gnode')
credits_node.addGeom(credits_geom)
credits_node_path = base.render.attachNewNode(credits_node)
credits_node_path.setTransparency(TransparencyAttrib.M_alpha)
credits_tex = base.loader.loadTexture('models/credits.jpeg')
credits_node_path.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
credits_node_path.setTexTransform(TextureStage.getDefault(), TransformState.makeHpr(LVecBase3f(0, -90, 180)))
credits_node_path.setTexOffset(TextureStage.getDefault(), .5, .5)
# credits_node_path.setTexOffset(TextureStage.getDefault(), 1.920, 1.920)
# credits_node_path.setTexScale(TextureStage.getDefault(), .5, 1, .5)
credits_node_path.setTexScale(TextureStage.getDefault(), 1/1.920/2, 1, 1/1.080/2)
credits_node_path.setTexProjector(TextureStage.getDefault(), base.render, credits_node_path)
credits_node_path.setTexture(credits_tex)
credits_node_path.set_pos_hpr(6.5, -4, 3.1, -90, 0, 180)
credits_node_path.set_scale(1.4)
credits_node_path.hide()
# credits_node_path.set_color_scale(0, 0, 0, 0)
# credits_node_path.set_color(1, 1, 1, 1)

# Events
stamp('Events')
with open(path+'/models/events.tsv') as file_object:
    # a = file_object.read()
    # print(a[5700:5800])
    # exit()
    csv_lines = file_object.readlines()
for csv_line in csv_lines[1:]:
    cols = csv_line.split('\t')
    if DEVEL:
        demo_parallel.append(eval(f'Sequence(Wait({cols[5]}), Func(print, "{csv_line[:-1]}"), {cols[6]})'))
    else:
        demo_parallel.append(eval(f'Sequence(Wait({cols[5]}), {cols[6]})'))

# Handshaking
stamp('Handshaking')
pos_shake_rope_vertices = []
hpr_shake_rope_vertices = []
for pos_shake_rope_vertices_i in range(round(demo_parallel.getDuration() * SHAKE_DEN)):
    pos_shake_rope_vertices.append((None, (
        pos_hpr_amplitudes[0] * Randomizer().randomRealUnit(),
        pos_hpr_amplitudes[1] * Randomizer().randomRealUnit(),
        pos_hpr_amplitudes[2] * Randomizer().randomRealUnit(),
    )))
for hpr_shake_rope_vertices_i in range(round(demo_parallel.getDuration() * SHAKE_DEN)):
    hpr_shake_rope_vertices.append((None, (
        pos_hpr_amplitudes[3] * Randomizer().randomRealUnit(),
        pos_hpr_amplitudes[4] * Randomizer().randomRealUnit(),
        pos_hpr_amplitudes[5] * Randomizer().randomRealUnit(),
    )))
pos_shake_rope_vertices[:STILL_START*SHAKE_DEN] = [(None, (0, 0, 0))]*STILL_START*SHAKE_DEN
hpr_shake_rope_vertices[:STILL_START*SHAKE_DEN] = [(None, (0, 0, 0))]*STILL_START*SHAKE_DEN
pos_shake_rope_vertices[STILL_STOP*SHAKE_DEN:] = [(None, (0, 0, 0))]*(len(pos_shake_rope_vertices)-STILL_STOP)*SHAKE_DEN
hpr_shake_rope_vertices[STILL_STOP*SHAKE_DEN:] = [(None, (0, 0, 0))]*(len(hpr_shake_rope_vertices)-STILL_STOP)*SHAKE_DEN
pos_shake_rope = Rope()
hpr_shake_rope = Rope()
pos_shake_rope.setup(4, pos_shake_rope_vertices)
hpr_shake_rope.setup(4, hpr_shake_rope_vertices)
pos_shake = pos_shake_rope.getPoints(round(demo_parallel.getDuration())*5000)
hpr_shake = hpr_shake_rope.getPoints(round(demo_parallel.getDuration())*5000)
# print(len(pos_shake))
handshaking_sequence = Sequence()
handshaking_sequence.append(LerpFunctionInterval(
    handshaking_lerp_function,
    fromData=0,
    toData=1,
    duration=len(pos_shake_rope_vertices),
))
demo_parallel.append(handshaking_sequence)

# print(demo_parallel.getDuration())
# exit()

# Set max delta
max_delta = 0

# Add and start main task
# base.taskMgr.doMethodLater(3, init_task, "init_task")

# taskMgr.setupTaskChain('chain', numThreads = None, tickClock = None,
#                        threadPriority = None, frameBudget = None,
#                        frameSync = None, timeslicePriority = None)
# base.taskMgr.add(main_task, "main_task")


base.taskMgr.add(main_task, "main_task")

# On screen text object
text_object = OnscreenText()

# Accept events
accept()

# bar.finish(), base.taskMgr.step(), base.taskMgr.step()
# bar.destroy()
set_card[24].remove_node()


if not DEVEL:
    base.disableMouse()
    accept_roping()

# has_force = False

# base.camLens.setAspectRatio(1920/1080)
# base.camLens.setAspectRatio(2560/1600)
# base.camLens.setAspectRatio(1.82)
# print(f'base.camLens.getAspectRatio(): {base.camLens.getAspectRatio()}')

stamp('Running demo')

base.run()



# Sequence(
#     Func(models['compo'].show),
#     Func(credits_node_path.show),
#     Func(clock.show),
#     Parallel(
#         beat_interval,
#         Func(filters.del_blur_sharpen),
#         Func(filters.del_cartoon_ink),
#         steam_interval,
#         Sequence(
#             LerpHprInterval(clock, 7, (-90, 0, 0), (0, 0, 0), blendType='easeOut'),
#             Wait(2),
#             LerpHprInterval(clock, 7, (-180, 0, 0), (-90, 0, 0), blendType='easeIn'),
#         ),
#         Sequence(
#             LerpColorScaleInterval(clock, 2, (1, 1, 1, 1), (1, 1, 1, 0), blendType='easeOut'),
#             Wait(12),
#             LerpColorScaleInterval(clock, 2, (1, 1, 1, 0), (1, 1, 1, 1), blendType='easeOut'),
#         ),
#         clock_interval,
#     )
# )