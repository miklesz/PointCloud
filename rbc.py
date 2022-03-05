# from direct.directbase.DirectStart import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import random

from panda3d.physics import LinearNoiseForce
from panda3d.physics import LinearJitterForce
from direct.particles.ForceGroup import ForceGroup
from direct.particles.Particles import Particles
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
# from panda3d.physics import DiscEmitter
# from panda3d.physics import LinearJitterForce, LinearRandomForce
# from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from direct.particles.ParticleEffect import ParticleEffect


def init_cube():
    litter_size = 16000
    particle_effect = ParticleEffect()
    particles = Particles()
    # Particles parameters
    particles.set_factory("PointParticleFactory")
    particles.set_renderer("PointParticleRenderer")
    particles.renderer.set_point_size(1)
    # particles.set_emitter("BoxEmitter")
    particles.set_emitter("RectangleEmitter")
    # particles.setPoolSize(litter_size*6*grow_time)
    particles.setPoolSize(litter_size)
    particles.setBirthRate(1/60)  # 1/60
    particles.setLitterSize(litter_size)
    # Factory parameters
    particles.factory.set_lifespan_base(10)
    particles.factory.set_terminal_velocity_base(400.0000)
    # Renderer parameters
    # particles.renderer.setStartColor(xel_a)
    # particles.renderer.setEndColor((1, 1, 1, 1))
    # particles.renderer.setBlendType(0)  # enumerator PP_ONE_COLOR = 0, PP_BLEND_LIFE = 1, PP_BLEND_VEL = 2
    # particles.renderer.setBlendMethod(0)  # LINEAR, CUBIC
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_NONE)
    # particles.renderer.setBlendMethod(BaseParticleRenderer.PP_NO_BLEND)  # LINEAR, CUBIC
    # particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_OUT)
    particles.renderer.set_alpha_mode(BaseParticleRenderer.PR_ALPHA_USER)
    particles.renderer.set_user_alpha(1.00)
    # particles.renderer.set_user_alpha(0.80)
    # Emitter parameters
    particles.emitter.set_emission_type(BaseParticleEmitter.ET_EXPLICIT)
    particles.emitter.set_offset_force(LVector3(0.0000, 0.0000, 0.0000))
    particles.emitter.set_explicit_launch_vector(LVector3(0.0000, 0.0000, 0.0000))

    # # Box parameters
    # particles.emitter.set_min_bound((-1, -1, -1))
    # particles.emitter.set_max_bound((+1, +1, +1))
    # Rectangle parameters
    particles.emitter.set_min_bound((-1, -1))
    particles.emitter.set_max_bound((+1, +1))


    particle_effect.add_particles(particles)

    # Force
    force_group = ForceGroup('zoom_random')
    # Force parameters
    # force = LinearJitterForce(1, 0)  # 0.1500 or 0.0750 - ADD THIS
    # force_group.addForce(LinearNoiseForce(1, 0))
    force_group.addForce(LinearJitterForce(.1, 0))  # 0.1500 or 0.0750 - ADD THIS
    #particle_effect.add_force_group(force_group)

    return particle_effect


# Init ShowBase
base = ShowBase()
base.enableParticles()

f = init_cube()
# f = base.loader.loadModel("box.egg")
print(f)
f.start(parent=base.render, renderParent=base.render)
# f.reparentTo(base.render)
print('done')

rbc = RigidBodyCombiner("rbc")
rbcnp = NodePath(rbc)
rbcnp.reparentTo(base.render)

# for i in range(650):
#     pos = Vec3(random.uniform(-100, 100),
#                random.uniform(+400, 600),
#                random.uniform(-100, 100))
#
#     # f = base.loader.loadModel("box.egg")
#     f = init_cube()
#     f.setPos(pos)
#     # f.start(parent=rbcnp, renderParent=rbcnp)
#     f.start(parent=base.render, renderParent=base.render)
#     # f.reparentTo(rbcnp)
#     # f.reparentTo(base.render)


rbc.collect()

base.render.ls()

base.setFrameRateMeter(True)
base.run()
