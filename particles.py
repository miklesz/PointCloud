# Related third party imports
from direct.particles.ForceGroup import ForceGroup
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.Particles import Particles
from panda3d.core import LPoint3
from panda3d.core import LVector3
from panda3d.core import LVector4
from panda3d.physics import BaseParticleEmitter
from panda3d.physics import BaseParticleRenderer
from panda3d.physics import LinearJitterForce
from panda3d.physics import LinearNoiseForce
from panda3d.physics import LinearVectorForce
# from panda3d.physics import LinearSourceForce
from panda3d.physics import LinearCylinderVortexForce
from panda3d.physics import PointParticleRenderer


def init_cube_particle_effect(point_size, x, y, z, xel_a, duration):
    # print(point_size, x, y, z, xel_a, duration)
    # litter_size = round(abs(400_000*x*y*z))  # 250  # 10  # 20
    # print(x, y, z, litter_size)
    # life_span = 10  # Default: 8
    litter_size = 7000  # 250  # 10  # 20  # 50000
    particle_effect = ParticleEffect(name='particle_cube')
    particles = Particles('display')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    # particles.setPoolSize(litter_size*6*grow_time)
    particles.setPoolSize(litter_size)
    particles.setBirthRate(0)  # 1/60
    particles.setLitterSize(litter_size)
    # Factory parameters
    particles.factory.set_lifespan_base(duration)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    particles.renderer.setStartColor(xel_a)
    # particles.renderer.setEndColor((1, 1, 1, 1))
    # particles.renderer.setBlendType(0)  # enumerator PP_ONE_COLOR = 0, PP_BLEND_LIFE = 1, PP_BLEND_VEL = 2
    # particles.renderer.setBlendMethod(0)  # LINEAR, CUBIC
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_NONE)
    # particles.renderer.setBlendMethod(BaseParticleRenderer.PP_NO_BLEND)  # LINEAR, CUBIC
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_USER)
    particles.renderer.set_user_alpha(.80)
    # particles.renderer.set_user_alpha(0.80)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.0000))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))
    # Box parameters
    min_bound = (-x/2, -y/2, -z/2)
    max_bound = (+x/2, +y/2, +z/2)
    particles.emitter.set_min_bound(min_bound)
    particles.emitter.set_max_bound(max_bound)
    particle_effect.add_particles(particles)

    # Force
    # force_group = ForceGroup('zoom_random')
    # Force parameters
    # force = LinearJitterForce(1, 0)  # 0.1500 or 0.0750 - ADD THIS
    # force_group.addForce(LinearNoiseForce(1, 0))
    # force_group.addForce(LinearJitterForce(10, 0))  # 0.1500 or 0.0750 - ADD THIS
    # particle_effect.add_force_group(force_group)

    return particle_effect


def init_display_particle_effect(point_size, min_x, min_z, max_x, max_z, xel_a):
    litter_size = 1  # 250  # 10  # 20
    grow_time = 5  # Default: 8, moje 4:
    life_span = 14.46 - (grow_time * 11) / 60 * 2  # Default: 8, moje: 16.42, 9.46
    # life_span = 12
    particle_effect = ParticleEffect()
    particles = Particles('display')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    particles.setPoolSize(litter_size*8*round(grow_time))  # 11
    particles.setBirthRate(1/30)  # 1/30 1/20
    particles.setLitterSize(litter_size)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    particles.renderer.set_start_color(xel_a)
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    # particles.renderer.set_user_alpha(0.45)
    # particles.renderer.set_user_alpha(0.80)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.0000))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))
    # Box parameters
    particles.emitter.set_min_bound((min_x, .98, min_z))  # .98
    particles.emitter.set_max_bound((max_x, .98, max_z))  # .98
    particle_effect.add_particles(particles)

    # Force
    force_group = ForceGroup('zoom_random')
    # Force parameters
    force_group.addForce(LinearJitterForce(.2, 0))  # 0.02 0.2 .15
    particle_effect.add_force_group(force_group)

    return particle_effect


def init_glow_particle_effect(point_size):
    litter_size = round(75/2)  # 2  # round(75/2)
    life_span = 1  # 0.7000
    particle_effect = ParticleEffect()
    particles = Particles('water')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    particles.setPoolSize(litter_size*60*life_span)  # litter_size*60*life_span, 2000
    particles.setBirthRate(1/60)  # 1/60
    particles.setLitterSize(litter_size)
    # particles.setLitterSpread(1)
    particles.setSystemLifespan(0.0000)
    particles.setLocalVelocityFlag(1)
    particles.setSystemGrowsOlderFlag(0)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.setLifespanSpread(0.2500)
    # particles.factory.setMassBase(2.0000)
    # particles.factory.setMassSpread(0.0100)
    # particles.factory.set_terminal_velocity_base(400.0000)
    # particles.factory.setTerminalVelocitySpread(0.0000)
    # Point factory parameters
    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_IN_OUT)
    particles.renderer.set_user_alpha(1.00)
    # particles.renderer.set_user_alpha(0.45)
    # Point parameters
    particles.renderer.setStartColor(LVector4(255/255, 227/255, 2/255, 1.00))
    particles.renderer.setEndColor(LVector4(1.00, 1.00, 1.00, 1.00))
    particles.renderer.setBlendType(PointParticleRenderer.PPONECOLOR)
    particles.renderer.setBlendMethod(BaseParticleRenderer.PPNOBLEND)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ETCUSTOM)
    particles.emitter.setAmplitude(1.0000)
    particles.emitter.setAmplitudeSpread(0.0000)
    # particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 4.0000))
    particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 0.0000))

    # particles.emitter.setExplicitLaunchVector(LVector3(1.0000, 0.0000, 0.0000))
    particles.emitter.setExplicitLaunchVector(LVector3(0.0000, 0.0000, 0.0000))

    particles.emitter.setRadiateOrigin(LPoint3(0.0000, 0.0000, 0.0000))

    # Box parameters
    # 63.573052499999996 m3 - 2 punkty na klatk??
    # particles.emitter.set_min_bound((2.5, 1.5, -1.5195))
    # particles.emitter.set_max_bound((7, 6, 1.61991))
    # 2393.8318415378426 m3 - 75 punkt??w na klatk??
    particles.emitter.set_min_bound((8.2763, -30.1388, 0.239379))
    particles.emitter.set_max_bound((27.1292, -8.2001, 6.02706))

    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('gravity')
    # force0 = LinearVectorForce(LVector3(0.0000, 0.0000, -1.0000), 25.0000, 1)
    # force0.setActive(1)
    # force_group.addForce(force0)
    force1 = LinearJitterForce(5.0000, 1)  # 3
    # force1 = LinearNoiseForce(3.0000, 1)
    force1.setActive(1)
    force_group.addForce(force1)
    particle_effect.addForceGroup(force_group)
    return particle_effect


def init_splash_particle_effect(point_size, pool_size):
    litter_size = 300
    life_span = 0.5000  # 0.5000
    particle_effect = ParticleEffect()
    particles = Particles('splash')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("DiscEmitter")
    particles.setPoolSize(pool_size)  # litter_size*60*life_span, 1000
    particles.setBirthRate(1/60)  # 1/60
    particles.setLitterSize(litter_size)
    particles.setLitterSpread(100)
    particles.setSystemLifespan(0.0000)
    particles.setLocalVelocityFlag(1)
    particles.setSystemGrowsOlderFlag(0)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    # particles.factory.setLifespanSpread(0.2500)
    particles.factory.setMassBase(2.0000)
    particles.factory.setMassSpread(0.0100)
    particles.factory.set_terminal_velocity_base(400.0000)
    particles.factory.setTerminalVelocitySpread(0.0000)
    # Point factory parameters
    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    particles.renderer.set_user_alpha(0.45)
    # Point parameters
    particles.renderer.setStartColor(LVector4(0.25, 0.90, 1.00, 1.00))
    particles.renderer.setEndColor(LVector4(1.00, 1.00, 1.00, 1.00))
    particles.renderer.setBlendType(PointParticleRenderer.PPONECOLOR)
    particles.renderer.setBlendMethod(BaseParticleRenderer.PPNOBLEND)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ETCUSTOM)
    particles.emitter.setAmplitude(1.0000)
    particles.emitter.setAmplitudeSpread(0.0000)
    particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 4.0000))
    # particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 0.0000))

    particles.emitter.setExplicitLaunchVector(LVector3(1.0000, 0.0000, 0.0000))
    # particles.emitter.setExplicitLaunchVector(LVector3(0.0000, 0.0000, 0.0000))

    particles.emitter.setRadiateOrigin(LPoint3(0, 0, 0))
    # Disc parameters
    particles.emitter.setRadius(0.0500)
    particles.emitter.setOuterAngle(356.1859)
    particles.emitter.setInnerAngle(0.0000)
    particles.emitter.setOuterMagnitude(2.0000)
    particles.emitter.setInnerMagnitude(1.0000)
    particles.emitter.setCubicLerping(0)
    # particles.emitter.set_min_bound((-2.89104, -2.71256, 0.879156))
    # particles.emitter.set_max_bound((2.76295, 2.03709, 0.879156))

    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('gravity')
    force0 = LinearVectorForce(LVector3(0.0000, 0.0000, -1.0000), 25.0000, 1)
    force0.setActive(1)
    force_group.addForce(force0)
    force1 = LinearJitterForce(3.0000, 1)
    force1.setActive(1)
    force_group.addForce(force1)
    particle_effect.addForceGroup(force_group)
    return particle_effect


def init_steam_particle_effect(
        point_size,
        litter_size=200,
        min_bound=(0, -8.0, 1.01067),
        max_bound=(7, -0.1, 1.01067),
):
    life_span = 4  # Default: 8
    particle_effect = ParticleEffect()
    particles = Particles('steam')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    particles.setPoolSize(litter_size*60*life_span)
    particles.setBirthRate(1/60)
    particles.setLitterSize(litter_size)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    particles.renderer.set_user_alpha(0.45)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.3800))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))
    # Box parameters
    particles.emitter.set_min_bound(min_bound)
    particles.emitter.set_max_bound(max_bound)
    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('vertex')

    # Force parameters
    linear_noise_force = LinearNoiseForce(0.1500, 0)
    linear_noise_force.setActive(True)
    force_group.addForce(linear_noise_force)
    particle_effect.add_force_group(force_group)

    return particle_effect


def init_water_particle_effect(point_size):
    litter_size = 800  # 900, 300 przy 4.5x2.5, 66.67/m2
    life_span = 1.2  # 0.5000
    particle_effect = ParticleEffect()
    particles = Particles('water')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    #
    particles.setPoolSize(round(litter_size*60*life_span))  # litter_size*60*life_span, 10000 przy 4.5x4.5, 2222.22/m2
    particles.setBirthRate(1/60)  # 1/60, 0.0200
    particles.setLitterSize(litter_size)
    particles.setLitterSpread(100)
    particles.setSystemLifespan(0.0000)
    particles.setLocalVelocityFlag(1)
    particles.setSystemGrowsOlderFlag(0)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.setLifespanSpread(0.2500)
    particles.factory.setMassBase(2.0000)
    particles.factory.setMassSpread(0.0100)
    particles.factory.set_terminal_velocity_base(400.0000)
    particles.factory.setTerminalVelocitySpread(0.0000)
    # Point factory parameters

    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    # particles.renderer.set_user_alpha(0.45)

    # Point parameters
    particles.renderer.setStartColor(LVector4(0.25, 0.90, 1.00, 1.00))
    particles.renderer.setEndColor(LVector4(1.00, 1.00, 1.00, 1.00))
    particles.renderer.setBlendType(PointParticleRenderer.PPONECOLOR)
    particles.renderer.setBlendMethod(BaseParticleRenderer.PPNOBLEND)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ETCUSTOM)
    particles.emitter.setAmplitude(1.0000)
    particles.emitter.setAmplitudeSpread(0.0000)
    # particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 4.0000))
    particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 0.0000))

    # particles.emitter.setExplicitLaunchVector(LVector3(1.0000, 0.0000, 0.0000))
    particles.emitter.setExplicitLaunchVector(LVector3(0.0000, 0.0000, 0.0000))

    particles.emitter.setRadiateOrigin(LPoint3(0.0000, 0.0000, 0.0000))
    # Box parameters
    # particles.emitter.set_min_bound((2.5, 1.5, 1.61991))
    # particles.emitter.set_max_bound((7, 6, 1.61991))
    particles.emitter.set_min_bound((13.2427, -8.1999, 13))
    particles.emitter.set_max_bound((26.8064, 13.069, 13))
    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('gravity')
    force0 = LinearVectorForce(LVector3(0.0000, 0.0000, -1.0000), 25.0000, 1)
    # force0 = LinearVectorForce(LVector3(0.0000, 0.0000, -0.0000), 25.0000, 1)
    force0.setActive(1)
    force_group.addForce(force0)
    force1 = LinearJitterForce(3.0000, 1)
    force1.setActive(1)
    force_group.addForce(force1)
    particle_effect.addForceGroup(force_group)
    return particle_effect


def init_dust_particle_effect(point_size):
    litter_size = 300  # 25, 100
    life_span = 1
    particle_effect = ParticleEffect()
    particles = Particles('dust')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    #
    particles.setPoolSize(round((litter_size+10)*60*(life_span+0.25)))
    # particles.setPoolSize(20000)
    # litter_size*60*life_span, 10000 przy 4.5x4.5, 2222.22/m2
    particles.setBirthRate(1/60)  # 1/60, 0.0200
    particles.setLitterSize(litter_size)
    particles.setLitterSpread(round(litter_size*0.4))
    particles.setSystemLifespan(0.0000)
    particles.setLocalVelocityFlag(1)
    particles.setSystemGrowsOlderFlag(0)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.setLifespanSpread(0.2500)
    particles.factory.setMassBase(2.0000)
    particles.factory.setMassSpread(0.0100)
    particles.factory.set_terminal_velocity_base(400.0000)
    particles.factory.setTerminalVelocitySpread(0.0000)
    # Point factory parameters

    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    # particles.renderer.set_user_alpha(1.00)
    particles.renderer.set_user_alpha(0.45)

    # Point parameters
    # particles.renderer.setStartColor(LVector4(184/255, 151/255, 122/255, 1.00))
    # particles.renderer.setStartColor(LVector4(0, 1, 0, 1))  # (0, 1, 0, 1)
    particles.renderer.setStartColor(LVector4(0.25, 0.90, 1.00, 1.00))
    particles.renderer.setEndColor(LVector4(1.00, 1.00, 1.00, 1.00))
    # particles.renderer.setEndColor(LVector4(1.00, 1.00, 1.00, 1.00))
    # particles.renderer.setBlendType(PointParticleRenderer.PPONECOLOR)
    # particles.renderer.setBlendMethod(BaseParticleRenderer.PPNOBLEND)

    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.setAmplitude(1.0000)
    particles.emitter.setAmplitudeSpread(0.0000)
    particles.emitter.setOffsetForce(LVector3(0, 0, 0))
    particles.emitter.setExplicitLaunchVector(LVector3(0, 0, 1))
    particles.emitter.setRadiateOrigin(LPoint3(0, 0, 0))

    # Box parameters
    particles.emitter.set_min_bound((-.02, -.02, .2))
    particles.emitter.set_max_bound((+.02, +.02, .2))

    particle_effect.add_particles(particles)

    # Force
    force_group = ForceGroup('gravity')

    force0 = LinearNoiseForce(2, 0)
    force0.setActive(1)
    force_group.addForce(force0)

    force1 = LinearJitterForce(2, 0)
    force1.setActive(1)
    force_group.addForce(force1)

    force4 = LinearCylinderVortexForce(1, 1, 7, 1, False)
    force4.setActive(1)
    force_group.addForce(force4)

    particle_effect.addForceGroup(force_group)
    return particle_effect


def init_greetings_particle_effect(point_size):
    litter_size = 500  # 250  # 10  # 20  # 900  # 600
    life_span = 2
    particle_effect = ParticleEffect()
    particles = Particles('greetings')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("BoxEmitter")
    particles.setPoolSize(round((litter_size*1.4)*60*(life_span+0.25)))
    # particles.setPoolSize(40000)
    particles.setBirthRate(1/60)
    particles.setLitterSize(litter_size)
    particles.setLitterSpread(round(litter_size * 0.4))
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    particles.factory.setLifespanSpread(0.2500)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    particles.renderer.setStartColor((1, 1, 1, 1))
    particles.renderer.setEndColor((153/255, 154/255, 149/255, 1))

    # particles.renderer.setStartColor((1, 1, 1, 1))
    # particles.renderer.setStartColor((13/255, 8/255, 244/255, 1))
    # particles.renderer.setEndColor((1, 1, 1, 1))
    # particles.renderer.setEndColor((13/255, 8/255, 244/255, 1))
    # particles.renderer.setEndColor((166/255, 28/255, 158/255, 1))
    particles.renderer.setBlendType(1)
    # particles.renderer.setBlendMethod(3)
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_IN_OUT)
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_USER)
    # particles.renderer.set_user_alpha(0.45)
    # particles.renderer.set_user_alpha(0.45)
    particles.renderer.set_user_alpha(0.80)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.0000))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))
    # Box parameters
    particles.emitter.set_min_bound((-4.75-1*1.2, -5.25-.4, 0.35-1*.8))  # -.4  # -5.31611
    particles.emitter.set_max_bound((-4.75+1*1.2, -5.25-.5, 0.35+1*.8))  # -.5  # -5.31611
    particle_effect.add_particles(particles)

    # Force
    force_group = ForceGroup('force_group')
    # Force parameters
    # force_group.addForce(LinearJitterForce(.2, 0))
    force_group.addForce(LinearJitterForce(1, 0))
    # force_group.addForce(LinearNoiseForce(.025, 0))
    particle_effect.add_force_group(force_group)

    return particle_effect


def init_ring_particle_effect(point_size):
    litter_size = 1000
    life_span = 0.30  # 0.5000
    particle_effect = ParticleEffect(name='ring')
    particles = Particles('ring')
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(point_size)
    particles.set_emitter("RingEmitter")
    particles.setPoolSize(1000)  # litter_size*60*life_span, 1000
    particles.setBirthRate(0)  # 1/60
    particles.setLitterSize(litter_size)
    particles.setLitterSpread(100)
    particles.setSystemLifespan(0.0000)
    particles.setLocalVelocityFlag(1)
    particles.setSystemGrowsOlderFlag(0)
    # Factory parameters
    particles.factory.set_lifespan_base(life_span)
    # particles.factory.setLifespanSpread(0.2500)
    particles.factory.setMassBase(2.0000)
    particles.factory.setMassSpread(0.0100)
    particles.factory.set_terminal_velocity_base(400.0000)
    particles.factory.setTerminalVelocitySpread(0.0000)
    # Point factory parameters
    # Renderer parameters
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    # particles.renderer.set_user_alpha(0.45)
    # Point parameters
    particles.renderer.setStartColor(LVector4(1, 1, 0, 1.00))
    particles.renderer.setEndColor(LVector4(1, 0, 0, 1.00))
    particles.renderer.setBlendType(PointParticleRenderer.PP_BLEND_LINEAR)
    particles.renderer.setBlendMethod(BaseParticleRenderer.PPNOBLEND)
    # Emitter parameters
    particles.emitter.setRadiateOrigin(LPoint3(0, 0, 0))
    particles.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
    # particles.emitter.setExplicitLaunchVector(LVector3(0.0000, 0.0000, 0.0000))
    particles.emitter.setAmplitude(0.0000)
    # particles.emitter.setAmplitudeSpread(0.0000)

    # particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 4.0000))
    # particles.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 0.0000))

    # particles.emitter.setExplicitLaunchVector(LVector3(1.0000, 0.0000, 0.0000))

    # particles.emitter.setRadiateOrigin(radiate_origin)
    # Disc parameters
    particles.emitter.setRadius(.75)
    # particles.emitter.setAngle(90)
    # particles.emitter.setOuterAngle(356.1859)
    # particles.emitter.setInnerAngle(0.0000)
    # particles.emitter.setOuterMagnitude(2.0000)
    # particles.emitter.setInnerMagnitude(1.0000)
    # particles.emitter.setCubicLerping(0)


    particle_effect.add_particles(particles)
    # Force
    force_group = ForceGroup('burn')
    force1 = LinearJitterForce(20, 1)
    force1.setActive(1)
    force_group.addForce(force1)
    particle_effect.addForceGroup(force_group)
    return particle_effect