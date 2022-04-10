# Standard library imports
from math import *
import platform
import sys

# Related third party imports
from direct.filter.CommonFilters import CommonFilters
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
done = False
# pos_hpr_amplitudes = [.005, .005, .005, .5, .5, .5]
pos_hpr_amplitudes = [.010 * (Randomizer().randomRealUnit() / 25 + 1) for a in range(3)] + \
                     [.500 * (Randomizer().randomRealUnit() / 25 + 1) for b in range(3)]
pos_hpr_offsets = [Randomizer().randomReal(2*pi) for i in range(6)]

# Constants
VERBOSE = True
# VERBOSE = False
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
        'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': True, 'cartoon_ink_separation': 2,
        'render_mode_perspective': False,
        'render_mode_thickness': 10,
    },
    {
        'preset': 2,
        'bloom': True, 'bloom_intensity': 1.0,
        'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
        'cartoon_ink': False, 'cartoon_ink_separation': 1,
        'render_mode_perspective': False,
        'render_mode_thickness': 2,
    },
    {
        'preset': 3,
        'bloom': True, 'bloom_intensity': 0.5,
        'blur_sharpen': True, 'blur_sharpen_amount': 1.0,
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
]
COLOR_SCALES = (
    ('Default', (127.5, 127.5, 127.5)),
    ('Oxford Blue', (15, 35, 71)),
    ('Rainbow Indigo', (28, 63, 110)),
    ('Lapis Lazuli', (46, 103, 160)),
    ('Carolina Blue', (90, 172, 207)),
    ('Key Lime', (239, 252, 147)),
    ('Dollar Bill', (128, 194, 113))
)


def change_mode_or_filter(mode_or_filter, change):
    if change is None:
        current_modes_and_filters[mode_or_filter] ^= True
    else:
        current_modes_and_filters[mode_or_filter] += change
    current_modes_and_filters['preset'] = None
    set_modes_and_filters()


def set_modes_and_filters(set_preset=None):
    global current_modes_and_filters
    if set_preset:
        # current_modes_and_filters = set_preset
        for key in set_preset:
            current_modes_and_filters[key] = set_preset[key]
    print(current_modes_and_filters)
    # quit()
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
    fov = cos(t * 30) * (1 - t) * 10 + 100  # sin
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
    base.accept('0', set_modes_and_filters, [PRESETS[0]])
    base.accept('1', set_modes_and_filters, [PRESETS[1]])
    base.accept('2', set_modes_and_filters, [PRESETS[2]])
    base.accept('3', set_modes_and_filters, [PRESETS[3]])
    base.accept('4', set_modes_and_filters, [PRESETS[4]])
    base.accept('5', set_modes_and_filters, [PRESETS[5]])
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
    base.accept('arrow_left', accept_yaw, [+2])
    base.accept('arrow_right', accept_yaw, [-2])
    base.accept('arrow_left-repeat', accept_yaw, [+2])
    base.accept('arrow_right-repeat', accept_yaw, [-2])
    base.accept('arrow_up', accept_pitch, [+2])
    base.accept('arrow_down', accept_pitch, [-2])
    base.accept('arrow_up-repeat', accept_pitch, [+2])
    base.accept('arrow_down-repeat', accept_pitch, [-2])


def main_task(task):
    global lasts
    global max_delta
    global text_object

    # Onscreen text
    text = f'''\
Yo FuCkErS!
time: {str(round(music.get_time(), 2))}
escape: sys.exit

# Setting Color Scales
a: avatarize (now: {COLOR_SCALES[current_modes_and_filters['color_scale'] % len(COLOR_SCALES)][0]})

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
{{/}}: inc/dec blur/sharpen (now: {round(current_modes_and_filters['blur_sharpen_amount'], 1)})

# Presets (now: {current_modes_and_filters['preset']})
0: set preset 0 (`None`)
1: set preset 1 (`Outdoor`)
2: set preset 2 (`Indoor 2px`)
3: set preset 3 (`Indoor 3px`)
4: set preset 4 (`Outdoor Perspective`)
5: set preset 5 (`Sitkowy`)
6: set preset 6 (`???`)
7: set preset 7 (`???`)
8: set preset 8 (`???`)
9: set preset 9 (`???`)

# Motion
m: set random position (once)
o: set random position (now: {pos_intervals})
r: roping (once)
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
'''
    if 'text_object' in globals():
        text_object.destroy()
    text_object = OnscreenText(text=text,
                               # pos=(-1.77, +.96),  # +.96
                               pos=(-base.getAspectRatio(), +.97),  # +.96
                               fg=(1, 1, 0, 1),
                               bg=(0, 0, 0, .5),
                               scale=0.038,  # 0.05
                               align=TextNode.ALeft)
    # OnscreenText(text=text,
    #                            pos=(-1.77, +.96),
    #                            fg=(1, 1, 0, 1),
    #                            bg=(0, 0, 0, .5),
    #                            scale=0.05,
    #                            align=TextNode.ALeft)

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

    # Tu stare, prymitywne włączanie motion blur
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
    steam_sequence = Sequence()
    steam_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(-2, 2, .1),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    # steam_sequence.append(ParticleInterval(
    #     particleEffect=init_steam_particle_effect(current_modes_and_filters['render_mode_thickness']),
    #     parent=office_model,
    #     worldRelative=True,
    #     duration=16,
    #     softStopT=8,
    #     cleanup=True,
    #     name='steam'
    # ))
    steam_sequence.start()


def roping_function(t, points, looks):
    i = int(len(points)*t)-1
    if i < 0:
        i = 0
    # print(i)
    spectator.set_pos(points[i])
    spectator.lookAt(looks[i])
    # spectator.lookAt(0, 0, 0)


def accept_roping():
    points = r.getPoints(len(vertices)*2*120)
    looks = l.getPoints(len(vertices)*2*120)
    roping_sequence = Sequence()
    roping_sequence.append(LerpFunc(
        function=roping_function,
        fromData=0,
        toData=1,
        duration=len(vertices)*2,
        extraArgs=[points, looks],
    ))
    roping_sequence.start()


def accept_water():
    # water_parallel = Parallel()
    water_sequence = Sequence()
    water_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(-2, 2, .1),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    # water_sequence.append(ParticleInterval(
    #     particleEffect=init_water_particle_effect(current_modes_and_filters['render_mode_thickness']),
    #     parent=office_model,
    #     worldRelative=True,
    #     duration=16,
    #     softStopT=8,
    #     cleanup=True,
    #     name='water'
    # ))
    # splash_interval = ParticleInterval(
    #     particleEffect=init_splash_particle_effect(current_modes_and_filters['render_mode_thickness']),
    #     parent=office_model,
    #     worldRelative=True,
    #     duration=1,
    #     cleanup=True,
    #     name='splash'
    # )
    water_sequence.start()
    # splash_interval.start()


def start_glow():
    glow_sequence = Sequence()
    glow_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(-2, 2, .1),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    # glow_sequence.append(ParticleInterval(
    #     particleEffect=init_glow_particle_effect(current_modes_and_filters['render_mode_thickness']),
    #     parent=office_model,
    #     worldRelative=True,
    #     duration=16,
    #     softStopT=8,
    #     cleanup=True,
    #     name='glow'
    # ))
    glow_sequence.start()


def start_display(display_particle_effect):
    display_particle_effect.start(parent=base.render)


def soft_stop_display(display_particle_effect):
    display_particle_effect.soft_stop()


def force_display(display_particle_effect):
    display_particle_effect.removeAllForces()
    display_particle_effect.soft_stop()
    force_group = ForceGroup('zoom')
    a = Randomizer().randomRealUnit()*.1
    # print(a)
    force_group.addForce(LinearNoiseForce(a, 0))  # 0.1500*2
    display_particle_effect.addForceGroup(force_group)


def zoom_function(t):
    fov_min = 66  # 66
    fov_max = 115  # 115
    fov = (fov_min-fov_max)*t+fov_max
    width = 3.5+t*1.5
    # width = 4
    base.camLens.setFov(fov)
    distance = 1.0-width/(2*tan(0.5*fov*2*pi/360))
    spectator.set_x(distance)
    # print(fov, distance, width)


def fov_function(t):
    fov_min = 66  # 66
    fov_max = 115  # 115
    fov = (fov_min-fov_max)*t+fov_max
    base.camLens.setFov(fov)
    # print(fov)


def init_display_sequence():
    # rbc = RigidBodyCombiner("rbc")
    # rigid = NodePath(rbc)
    # rigid.reparentTo(base.render)

    # Remove point cloud
    # office_model.remove_node()
    # print(office_model)

    # Read image
    my_image = PNMImage(Filename("icons/icon-32.png"))

    # Initialise sequence
    zoom_sequence = Sequence()
    zoom_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(-2, 2, .1),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))

    # Append particle effects
    display_particle_effects = []
    for x in range(my_image.getXSize()):
        for z in range(my_image.getYSize()):
            min_x = x / my_image.getXSize() * 2 - 1
            min_z = z / my_image.getYSize() * 2 - 1
            max_x = (x+1) / my_image.getXSize() * 2 - 1
            max_z = (z+1) / my_image.getYSize() * 2 - 1
            xel_a = my_image.getXelA(x, z)
            if xel_a[3] > .5:
                display_particle_effects.append(init_display_particle_effect(
                    current_modes_and_filters['render_mode_thickness'],
                    min_x,
                    min_z,
                    max_x,
                    max_z,
                    xel_a
                ))
    print('len(display_particle_effects):', len(display_particle_effects))
    # quit()

    # Append functions
    for display_particle_effect in display_particle_effects:
        zoom_sequence.append(Func(start_display, display_particle_effect))

    # Append wait
    zoom_sequence.append(Wait(4))

    # Append particle outs
    for display_particle_effect in display_particle_effects:
        zoom_sequence.append(Func(force_display, display_particle_effect))
        # print(display_particle_effect.getParticlesDict())

    # Start sequence
    zoom_sequence.start()
    # rbc.collect()

    # time.sleep(5)
    # base.render.ls()


def dissolve(t, cube_object):
    cube_object.removeAllForces()
    force_group = ForceGroup()
    force_group.addForce(LinearJitterForce(t*25, 0))
    cube_object.addForceGroup(force_group)
    # cube_object.setTransparency(TransparencyAttrib.M_alpha)
    cube_object.setAlphaScale(1-t)
    # cube_object.setColorScale(1, 1, 1, (1-t))


def start_zoom():
    # fov_min = 66
    # fov_max = 115
    duration = 1
    rotation = 180
    # Sequence just to avoid warnings!
    zoom_prepare_parallel = Parallel()
    zoom_prepare_parallel.append(LerpFunc(fov_function, fromData=0, toData=1, duration=2, blendType='easeInOut'))
    zoom_prepare_parallel.append(init_pos_interval((1.0-5/(2*tan(0.5*66*2*pi/360)), 0, 0), duration=2))
    zoom_sequence = Sequence()
    zoom_sequence.append(zoom_prepare_parallel)

    # print(len(display_particle_effects))
    # for display_particle_effect in display_particle_effects:
    # zoom_sequence.append(Func(start_display, init_cube(1, 1, 1, (1, 0, 0, 1))))
    for cube_number in range(16):
        cube = init_cube_particle_effect(
            current_modes_and_filters['render_mode_thickness'],
            Randomizer().randomReal(.5)+.5,
            Randomizer().randomReal(.5)+.5,
            Randomizer().randomReal(.5)+.5,
            (Randomizer().randomReal(.5)+.5, Randomizer().randomReal(.5)+.5, Randomizer().randomReal(.5)+.5, 1),
            duration
        )
        cube_parallel = Parallel()
        cube_parallel.append(LerpFunc(
            function=dissolve,
            fromData=0,
            toData=1,
            duration=duration,
            blendType='easeIn',
            extraArgs=[cube],
        ))
        cube_parallel.append(ParticleInterval(
            particleEffect=cube,
            parent=base.render,
            worldRelative=False,
            duration=duration,
            cleanup=True,
        ))
        start_h = Randomizer().randomInt(360)
        start_p = Randomizer().randomInt(360)
        start_r = Randomizer().randomInt(360)
        cube_parallel.append(LerpHprInterval(
            nodePath=cube,
            duration=duration,
            hpr=(
                start_h+Randomizer().randomRealUnit()*rotation,
                start_p+Randomizer().randomRealUnit()*rotation,
                start_r+Randomizer().randomRealUnit()*rotation,
            ),
            startHpr=(start_h, start_p, start_r),
        ))
        zoom_sequence.append(cube_parallel)
        # print(cube.getParticlesDict())
        # cube.analyze()
        # cube.setTransparency(TransparencyAttrib.M_alpha)
        # cube.setAlphaScale(0.2)
        # cube.hide()
        # cube.setScale(5)

    # zoom_sequence.append(Wait(2))
    # zoom_sequence.append(LerpFunc(zoom_function, fromData=1, toData=0, duration=2, blendType='easeInOut'))

    # for display_particle_effect in display_particle_effects:
    #     zoom_sequence.append(Func(force_display, display_particle_effect))

    # zoom_sequence.append(LerpFunc(zoom_function, fromData=0, toData=1, duration=1, blendType='easeInOut'))
    # zoom_sequence.append(LerpFunc(zoom_function, fromData=1, toData=0, duration=1, blendType='easeInOut'))
    # zoom_sequence.append(LerpFunc(zoom_function, fromData=0, toData=1, duration=1, blendType='easeInOut'))
    # zoom_sequence.append(LerpFunc(zoom_function, fromData=1, toData=0, duration=1, blendType='easeInOut'))
    # start_display()
    zoom_sequence.start()
    # base.render.analyze()
    # display_particle_effects[0].analyze()
    # model.analyze()
    # point_cloud.analyze()
    # display_interval = LerpFunc(display, fromData=0, toData=1, duration=10)


def set_fog_exp_density(t, fog):
    fog.setExpDensity(t)


def set_background_color(t, color, set_preset):
    base.set_background_color(color[0]*t, color[1]*t, color[2]*t)
    set_modes_and_filters(PRESETS[0])
    set_modes_and_filters(PRESETS[set_preset])


def trainspotting_lerp_function(t):
    base.cam.set_scale(1, 1-(t*.99), 1)


def accept_trainspotting():
    trainspotting_sequence = Sequence()
    trainspotting_sequence.append(LerpPosHprInterval(
        nodePath=spectator,
        pos=(-2, 2, .1),
        hpr=(90, 0, 0),
        duration=2,
        blendType='easeInOut',
    ))
    trainspotting_sequence.append(LerpFunctionInterval(
        trainspotting_lerp_function,
        fromData=0,
        toData=1,
        duration=4,
        blendType='easeInOut',
    ))
    trainspotting_sequence.append(LerpFunctionInterval(
        trainspotting_lerp_function,
        fromData=1,
        toData=0,
        duration=4,
        blendType='easeInOut',
    ))
    trainspotting_sequence.start()


def handshaking_lerp_function(t):
    global pos_hpr_amplitudes
    global pos_hpr_offsets
    args = []
    for i in range(6):
        pos_hpr_amplitudes[i] *= Randomizer().randomRealUnit() / 25 + 1  # 20?
        pos_hpr_offsets[i] *= Randomizer().randomRealUnit() / 25 + 1  # 30?
        args.append(sin(pi * t + pos_hpr_offsets[i]) * pos_hpr_amplitudes[i])
    base.cam.set_pos_hpr(*args)


def accept_handshaking():
    handshaking_sequence = Sequence()
    handshaking_sequence.append(LerpFunctionInterval(
        handshaking_lerp_function,
        fromData=0,
        toData=64,
        duration=64,
    ))
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

if VERBOSE:
    print("PandaSystem.version_string:", PandaSystem.version_string)

# Load music
# music = base.loader.loadSfx("music/perka.ogg")
music = base.loader.loadSfx("music/kramsta.ogg")

# Set window
fullscreen = False
props = WindowProperties()
props.setIconFilename('icons/icon-256.png')
props.setTitle('Kramsta by Damage')
base.win.request_properties(props)
toggle_fullscreen()

# Setting background color
base.setBackgroundColor(0, 0, 0)

# Load models and make point-clouds
models = []
clouds = []
model_dict = {
    'podium': {'ext': 'obj', 'pos_hpr': (0, -20, 0, 0, 90, 0)},
    'sign': {'ext': 'obj', 'pos_hpr': (30, -10, 0, 0, 90, 0)},
    'bar_rtab_': {'ext': 'obj', 'pos_hpr': (0, 0, 0, 0, 0, 0)},
    'entrance': {'ext': 'obj', 'pos_hpr': (10, 0, 0, 0, 90, 0)},
    'room_1': {'ext': 'obj', 'pos_hpr': (-10, 0, 0, 0, 90, 0)},
    'room_2': {'ext': 'obj', 'pos_hpr': (10, 10, 0, 0, 90, 0)},
    'room_3': {'ext': 'obj', 'pos_hpr': (0, 10, 0, 0, 90, 0)},
    'wc': {'ext': 'obj', 'pos_hpr': (-10, 10, 0, 0, 90, 0)},
    'garden': {'ext': 'obj', 'pos_hpr': (20, 20, 0, 0, 90, 0)},
    'hall_dae': {'ext': 'dae', 'pos_hpr': (0, 20, 0, 0, 90, 0)},
    'compo': {'ext': 'obj', 'pos_hpr': (-20, 0, 0, 0, 90, 0)},
    'garden_large': {'ext': 'obj', 'pos_hpr': (-30, -30, 0, 0, 90, 0)},
}

for model_key in model_dict:
    print(model_key, model_dict[model_key])
    ext = model_dict[model_key]['ext']
    model_dict[model_key]['model'] = base.loader.loadModel(f'models/{model_key}/textured_output.{ext}')
    model_dict[model_key]['model'].set_pos_hpr(*model_dict[model_key]['pos_hpr'])
    model_dict[model_key]['model'].reparentTo(base.render)
    model_dict[model_key]['cloud'] = model_dict[model_key]['model'].find("**/+GeomNode")
    for geom in model_dict[model_key]['cloud'].node().modify_geoms():
        geom.make_points_in_place()

# Set frame rate meter
base.set_frame_rate_meter(True)

# print('base.model.getTightBounds():', office_model.getTightBounds())


if VERBOSE:
    base.render.ls()
    base.render.analyze()

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

# model.setColorScale(15/255*2, 35/255*2, 71/255*2, 1)

# Set camera lens field of view
base.camLens.setFov(115)
# base.camLens.fov = 100

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

spectator.set_z(+7)
spectator.set_p(-90)

look_color = (1, .5, 1, 1)
with open('models/mopaths.csv') as file_object:
    csv_lines = file_object.readlines()
vertices = []
look_vertices = []
for csv_line in csv_lines[1:]:
    cols = csv_line.split(',')
    vertices.append((None, (float(cols[3]), float(cols[4]), float(cols[5]))))
    look_vertices.append({'point': (float(cols[6]), float(cols[7]), float(cols[8])), 'color': look_color})

r = Rope()
r.setup(4, vertices)
r.ropeNode.setThickness(2)
r.ropeNode.setNumSubdiv(2*120)
r.setPos(0, 0, 0)
r.reparentTo(base.render)
r.recompute()

l = Rope()
l.setup(4, look_vertices)
l.ropeNode.setUseVertexColor(1)
l.ropeNode.setThickness(2)
l.ropeNode.setNumSubdiv(2*120)
l.setPos(0, 0, 0)
l.reparentTo(base.render)
l.recompute()

# points = r.getPoints(5 * 120 * 100)

# Append position intervals
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
beat_interval = LerpFunc(beat, fromData=0, toData=1, duration=period/4)
beat_count = 0

# print(current_modes_and_filters['color_scale'])
# print(current_modes_and_filters)
# quit()

# Render modes and common filters
filters = CommonFilters(base.win, base.cam)
for preset in PRESETS[::-1]:
    set_modes_and_filters(preset)

base.enableParticles()

# display_sequence = init_display_sequence()

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
