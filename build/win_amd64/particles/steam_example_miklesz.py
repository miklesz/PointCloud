#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Last Updated: 2015-03-13
#
# This tutorial shows how to take an existing particle effect taken from a
# .ptf file and run it in a general Panda project.

from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import LPoint3, LVector3
from panda3d.core import Filename
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText
from direct.filter.CommonFilters import CommonFilters
import sys
from direct.interval.IntervalGlobal import *

HELP_TEXT = """
1: Load Steam
2: Load Dust
3: Load Fountain
4: Load Smoke
5: Load Smokering
6: Load Fireish
7: Load Evaporation
8: Load Fireflies
ESC: Quit
"""

class ParticleDemo(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Standard title and instruction text
        self.title = OnscreenText(
            text="Panda3D: Tutorial - Particles",
            parent=base.a2dBottomCenter,
            style=1, fg=(1, 1, 1, 1), pos=(0, 0.1), scale=.08)
        self.escapeEvent = OnscreenText(
            text=HELP_TEXT, parent=base.a2dTopLeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.06),
            align=TextNode.ALeft, scale=.05)

        # More standard initialization
        self.accept('escape', sys.exit)
        self.accept('1', self.loadParticleConfig, ['steam.ptf'])
        self.accept('2', self.loadParticleConfig, ['dust.ptf'])
        self.accept('3', self.loadParticleConfig, ['fountain.ptf'])
        self.accept('4', self.loadParticleConfig, ['smoke.ptf'])
        self.accept('5', self.loadParticleConfig, ['smokering.ptf'])
        self.accept('6', self.loadParticleConfig, ['fireish.ptf'])
        self.accept('7', self.loadParticleConfig, ['evaporation_geom.ptf'])
        self.accept('8', self.loadParticleConfig, ['evaporation_point.ptf'])

        self.accept('escape', sys.exit)
        base.disableMouse()
        base.camera.setPos(0, -20, 10)
        base.camLens.setFov(25)
        base.setBackgroundColor(0, 0, 0)

        base.setFrameRateMeter(True)
        # self.ball = loader.loadModel("ball.dae")

        # This command is required for Panda to render particles
        base.enableParticles()
        self.t = loader.loadModel("teapot")
        print(type(self.t.node()))
        self.t.setPos(0, 10, 0)
        # self.t.set_scale(0.01)
        self.t.reparentTo(render)
        self.setupLights()
        self.p = ParticleEffect()
        self.loadParticleConfig('evaporation_collision.ptf')
        # self.render.setRenderModeThickness(10)

        base.cam.look_at(self.t)

        # rotate_interval = LerpHprInterval(nodePath=self.t, duration=10, hpr=(0, 0, 0))
        # rotate_interval.loop()

        # self.render.setRenderModeThickness(10)

        # filters = CommonFilters(base.win, base.cam)
        # filters.setBloom(blend=(1.0, 1.0, 1.0, 1.0),
        #                  mintrigger=0.0,
        #                  desat=0,
        #                  intensity=2.0,
        #                  size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
        # filters.setCartoonInk()
        # base.render.setShaderAuto()

    def loadParticleConfig(self, filename):
        # Start of the code from steam.ptf
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(filename))
        # Sets particles to birth relative to the teapot, but to render at
        # toplevel
        self.p.start(self.t)
        # self.p.start(base.render)
        # self.p.setPos(3.000, 0.000, 2.250)
        self.p.setPos(0.000, 0.000, 0.000)

    # Setup lighting
    def setupLights(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.4, .4, .35, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 8, -2.5))
        directionalLight.setColor((0.9, 0.8, 0.9, 1))
        # Set lighting on teapot so steam doesn't get affected
        self.t.setLight(self.t.attachNewNode(directionalLight))
        self.t.setLight(self.t.attachNewNode(ambientLight))

demo = ParticleDemo()
demo.run()
