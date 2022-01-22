# Curved, Motion Paths, Ropes:
# https://discourse.panda3d.org/t/solved-create-curve-as-specified-by-movement-of-camera/11580/8
# https://docs.panda3d.org/1.10/python/programming/physics/bullet/softbody-rope

# import gl

from panda3d.core import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase
from math import sin, cos, pi
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import Randomizer
from direct.showbase.RandomNumGen import RandomNumGen, randHash

from panda3d.core import GraphicsWindow

from panda3d.core import loadPrcFileData
# loadPrcFileData('', 'fullscreen #t')

from panda3d.core import PandaSystem
print("Panda version:", PandaSystem.getVersionString())

from MIDI import MIDIFile
name = 'music/MIDI perka.mid'
# name = 'music/MIDI perka melody.mid'
c = MIDIFile(name)
print(name)
c.parse()
track = c[0]
track.parse()

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        print(self.win.gsg.driver_vendor)
        print(self.win.gsg.driver_renderer)

        # self.music = self.loader.loadSfx("music/PrevForMiklesz.ogg")
        self.music = self.loader.loadSfx("music/perka.ogg")
        # self.music = self.loader.loadSfx("music/co sekunde.wav")

        # print(self.win.getGsg().getSupportsBasicShaders())
        # quit()

        # loadPrcFileData('', 'win-size 1024 768')
        # loadPrcFileData('', 'fullscreen #f')

        # w, h = 1024, 768
        #
        # props = WindowProperties()
        # props.setSize(w, h)
        # props.setFullscreen(True)
        # # props.fullscreen = True
        # self.win.requestProperties(props)

        xSize=self.pipe.getDisplayWidth()
        ySize=self.pipe.getDisplayHeight()
        props = WindowProperties()
        props.setSize(xSize,ySize)
        props.setFixedSize(1)
        props.setTitle('Amiga Rulez!')
        self.win.requestProperties(props)

        # Setting background color
        self.setBackgroundColor(0, 0, 0)

        # self.model = self.loader.loadModel("models/panda-model")
        # self.model = self.loader.loadModel("models/room.ply")
        # self.model = self.loader.loadModel("models/220101-221614-Mesh.ply")
        # self.model = self.loader.loadModel("models/220101-221614.ply")
        # self.model = self.loader.loadModel("models/Modelar-2022-Jan-01-2.ply")
        # self.model = self.loader.loadModel("models/Modelar-2022-Jan-01.e57")
        # self.model = self.loader.loadModel("models/Modelar-2022-Jan-01.ply")
        # self.model = self.loader.loadModel("models/Modelar-2022-Jan-01.stl")
        # self.model = self.loader.loadModel("models/Modelar-2022-Jan-01.usdz")
        # self.model = self.loader.loadModel("models/poly.glb")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221158.fbx")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221209/scaniverse-20210101-221209.obj")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221220.glb")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221228.usdz")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221237.stl")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221244.ply")
        # self.model = self.loader.loadModel("models/scaniverse-20210101-221257.las")
        # self.model = self.loader.loadModel("models/table.e57")
        # self.model = self.loader.loadModel("models/table.ply")
        # self.model = self.loader.loadModel("models/duzy2.ply")
        # self.model = self.loader.loadModel("models/pokoj.obj")
        # self.model = self.loader.loadModel("models/textured_output.obj")
        # self.model = self.loader.loadModel("models/Chrobrego_3D.ply")
        # self.model = self.loader.loadModel("models/Chrobrego_PC.ply")
        # self.model = self.loader.loadModel("models/no_opt_pc.ply")
        # self.model = self.loader.loadModel("models/no_opt_col_mesh.ply")
        # self.model = self.loader.loadModel("models/opt_col_mesh.ply")

        self.model = self.loader.loadModel("models/office.ply")
        # self.model = self.loader.loadModel("models/220102-151206.ply")
        # self.model = self.loader.loadModel("models/220102-151909.ply")

        # self.model.showTightBounds()
        self.model.reparentTo(self.render)
        self.model.ls()
        print("\nself.model.getTightBounds():")
        print(self.model.getTightBounds())
        print("\nself.model.analyze():")
        self.model.analyze()

        self.setFrameRateMeter(True)

        self.point_cloud = self.model.find("**/+GeomNode")
        self.point_cloud.setRenderModeThickness(2)  # from example: 5, good looking: 3
        # self.point_cloud.setRenderModePerspective(True, 100)
        # self.point_cloud.setRenderModeWireframe(100)

        for geom in self.point_cloud.node().modify_geoms():
            geom.make_points_in_place()

        # self.ball = self.loader.loadModel("../Damage/ball.dae")
        # self.ball.reparentTo(self.render)
        #
        # spotlight = Spotlight('spotlight')
        # self.spot = self.render.attachNewNode(spotlight)
        # self.spot.setPos(-25, -15, 30)   # -27.4554, -16.2955, 33.2832
        # self.spot.lookAt(self.ball)
        # self.render.setLight(self.spot)
        #
        # self.render.setDepthOffset(-3)

        # Filters: https://docs.panda3d.org/1.10/python/programming/render-to-texture/common-image-filters
        print(self.win.getGsg().getSupportsBasicShaders())
        self.filters = CommonFilters(self.win, self.cam)
        self.filters.setBloom(blend=(0.3,0.4,0.3,1.0), mintrigger=0.0, desat=0, intensity=2.0, size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
        # self.filters.setCartoonInk()
        # self.filters.setVolumetricLighting(caster=self.point_cloud, numsamples=64, density=1.0, decay=0.98, exposure=1.0)
        # filters.setInverted()
        # self.filters.setBlurSharpen(2.0)
        # filters.setAmbientOcclusion()
        # filters.setGammaAdjust(1.5)

        self.render.setShaderAuto()

        self.camLens.setFov(100)

        #self.cam.setPos(-1.2, -1.0, +0.0)
        # self.cam.setPos(-1, +1, 0)
        # self.cam.setHpr(+270, 0, 0)

        # self.cam.setPos(0, 0, 0)
        # self.cam.setHpr(0, 0, 0)


        # self.cam.lookAt(+2.0, 0, 0)

        #self.cam.setHpr(-45, 0, 0)

        # self.wireframeOn()
        # self.toggleShowVertices()
        # self.toggleTexture()

        # Try full-screen
        # print("Full-screen:", WindowProperties.fullscreen(True))
        # print("Full-screen:", self.win.getProperties())
        # props = WindowProperties(self.win.getProperties())
        # print("Full-screen:", props)
        # props.setFullscreen(True)
        # props = WindowProperties(self.win.getProperties())
        # print("Full-screen:", props)
        # print("Full-screen:", self.win.isFullscreen())

        # new_wp = WindowProperties()
        # new_wp.setFullscreen(True)
        # new_wp.setSize(800, 600)


        # X, Y, Z, H, P, R, Scale Y, FOV
        self.currents= [0, 0, 0, 0, 0, 0, 1, self.camLens.getFov()[0]]
        self.lasts   = [0, 0, 0, 0, 0, 0, 1, self.camLens.getFov()[0]]
        self.deltas  = [0, 0, 0, 0, 0, 0, 0, 0]
        self.weights = [.2, .2, .2, .2, .2, .2, 50, .1]
        self.delta = 0

        # i = LerpPosInterval(self.cam,
        #                     5,
        #                     (2, -1.3, 0),
        #                     startPos=None,
        #                     other=None,
        #                     blendType='easeInOut',
        #                     bakeInStart=1,
        #                     fluid=0,
        #                     name=None)

        # X = -2.5..+2.7
        # Y = -1.2..+0.4
        # Z = -1.7..+0.4

        period = 120/125

        # i0 = LerpPosInterval(nodePath=self.cam, duration=period, pos=(-1.2, +1.0, +0.0), blendType='easeOut')
        # i1 = LerpPosInterval(nodePath=self.cam, duration=period, pos=(+0.8, +1.0, +0.0), blendType='easeOut')
        # i2 = LerpPosInterval(nodePath=self.cam, duration=period, pos=(+0.8, -1.0, +0.0), blendType='easeOut')
        # i3 = LerpPosInterval(nodePath=self.cam, duration=period, pos=(-1.2, -1.0,  0.0), blendType='easeOut')

        # i0 = LerpPosInterval(nodePath=self.cam, duration=period, pos=( 0, -1,  0))
        # i1 = LerpPosInterval(nodePath=self.cam, duration=period, pos=(-1,  0,  0))
        # i2 = LerpPosInterval(nodePath=self.cam, duration=period*8, pos=( 0,  1,  0))
        # i3 = LerpPosInterval(nodePath=self.cam, duration=period, pos=( 1,  0,  0))

        # pan = LerpPosHprInterval(nodePath=self.cam, duration=period*8, pos=(+1, +1, 0), hpr=())
        # pan = LerpPosInterval(nodePath=self.cam, duration=period*8, pos=(+1, +1, 0))

        # i0 = LerpPosInterval(nodePath=self.cam, duration=period/2, pos=(-1.2, +1.0, +0.0), blendType='easeOut')
        # i1 = LerpPosInterval(nodePath=self.cam, duration=period/2, pos=(+0.8, +1.0, +0.0), blendType='easeOut')
        # i2 = LerpPosInterval(nodePath=self.cam, duration=period/2, pos=(+0.8, -1.0, +0.0), blendType='easeOut')
        # i3 = LerpPosInterval(nodePath=self.cam, duration=period/2, pos=(-1.2, -1.0,  0.0), blendType='easeOut')

        self.dummy = self.render.attachNewNode("dummy")
        mySequence = Sequence()
        rn = Randomizer()
        old_hpr = self.cam.getHpr()
        for interval_index in range(64):
            pos1 = (rn.randomRealUnit()*4.79, rn.randomRealUnit()*3.81, rn.randomReal(2.66-1.75))
            self.dummy.setPos(pos1)
            self.dummy.lookAt(0, 0, 0)
            new_hpr = self.dummy.getHpr()

            if new_hpr[0]-old_hpr[0]>180:
                new_hpr[0]-=360

            if new_hpr[0]-old_hpr[0]<-180:
                new_hpr[0]+=360


            if abs(new_hpr[0]-old_hpr[0])>180:
                overfull = True
            else:
                overfull = False

            print('old_hpr:', old_hpr, 'new_hpr:', new_hpr, 'overfull:', overfull)
            old_hpr = new_hpr
            interval = LerpPosHprInterval(nodePath=self.cam, duration=period, pos=pos1, hpr=new_hpr, blendType='easeOut')
            mySequence.append(interval)
        # quit()

        # i1 = LerpPosHprInterval(nodePath=self.cam, duration=period/2, pos=(+0.8, +1.0, +0.0), hpr=(-90*2-45, 0, 0), blendType='easeOut')
        # i2 = LerpPosHprInterval(nodePath=self.cam, duration=period/2, pos=(+0.8, -1.0, +0.0), hpr=(-90*3-45, 0, 0), blendType='easeOut')
        # i3 = LerpPosHprInterval(nodePath=self.cam, duration=period/2, pos=(-1.2, -1.0,  0.0), hpr=(-90*4-45, 0, 0), blendType='easeOut')

        # i0 = LerpHprInterval(nodePath=self.cam, duration=period, hpr=(90*1, 0, 0))
        # i1 = LerpHprInterval(nodePath=self.cam, duration=period, hpr=(90*2, 0, 0))
        # i2 = LerpHprInterval(nodePath=self.cam, duration=period, hpr=(90*3, 0, 0))
        # i3 = LerpHprInterval(nodePath=self.cam, duration=period, hpr=(90*4, 0, 0))
        # i4 = LerpHprInterval(nodePath=self.cam, duration=period, hpr=(90*5, 0, 0))

        def beat(t):
            # Do something based on t.
            fov = cos(t * 30) * (1 - t) * 10 + 100  # sin
            self.camLens.setFov(fov)
            # print('beat', t)

        i = LerpFunc(beat, fromData=0, toData=1, duration=period/4)
        # i = LerpFunc(beat, fromData=0, toData=1, duration=period/4, blendType='easeOut')

        self.beat_start = 0
        def beat_start(task):
            # print('beat start', self.beat_start)
            self.beat_start += 1
            i.start()

        # mySequence = Sequence(i0, i1, i2, i3)
        # mySequence = Sequence(i2)
        # mySequence = Sequence(i0, i1, i2, i3, i4)
        # mySequence = Sequence(i0, i, i1, i, i2, i, i3, i)

        # print(self.music.status())
        while self.music.status() != AudioSound.PLAYING:
            self.music.play()
        # print(self.music.status())
        # print(AudioSound.PLAYING)

        print('Starting music, time:', self.music.getTime())

        # mySequence.loop()
        mySequence.start()
        # pan.start()

        # beat_start(0)

        t0 = False
        time = 0
        prev_time = 0
        for ev in track:
            # print(ev)
            if 'NOTE_ON' in str(ev):
                if not t0:
                    t0 = ev.time
                # time = (ev.time - t0) / 192 * period
                # print(time, ev.message.note)
                if str(ev.message.note)=='C3' and (time-prev_time)>=period*2:
                    # pass
                    # print(time, ev.message.note)
                    #self.taskMgr.doMethodLater(time, beat_start, 'beat')
                    prev_time = time

        for range_time in range(16, 64, 1):
            time = range_time * period
            print(time)
            self.taskMgr.doMethodLater(time, beat_start, 'beat')

        self.textObject = OnscreenText(text=str(round(self.music.getTime(), 2)), pos=(-1.8, +.9), fg=(1, 0.5, 0.5, 1),
                                  bg=(0, 0, 0, 1), scale=0.07, align=TextNode.ALeft)
        self.taskMgr.add(self.myTask, "myTask")

        self.max_delta = 0

        print('Starting demo, time:', self.music.getTime())
        # quit()

    def myTask(self, task):

        # print(self.music.getTime())
        self.textObject.destroy()
        self.textObject = OnscreenText(text=str(round(self.music.getTime(),2)), pos=(-1.8, +.9), fg=(1, 0.5, 0.5, 1), bg=(0, 0, 0, 1), scale=0.07, align=TextNode.ALeft)

        # print(self.cam.getPos(), self.cam.getHpr())
        # print(self.camLens.getFov()[0])

        # print(self.pos)
        # print(self.hpr)
        # self.hpr = self.point_cloud.getScale()
        # self.hpr = self.model.getScale()
        # print(self.scale)
        # self.camLens.setFov(task.time+1)

        # v = cos((task.time+pi/2)*1*2)+1
        # self.filters.setBlurSharpen(v)
        # self.filters.setBlurSharpen(100)

        # self.model.setScale(1, 1+task.time, 1)

        # angle = sin(task.time*1)*90
        # self.cam.setH(angle)
        # self.cam.lookAt(+0.0, -0.0, 0.0)  #-1
        # self.cam.headsUp(+0.0, -0.0, -1.0)
        # self.cam.setPos(angle/100, -1.3, 0)

        decay = 1
        # if task.time % 1 < .5:
        #     decay = ( 1 - (task.time % 1)*2 ) * 2
        # else:
        #     decay = 0
        # fov = sin(task.time*60)*decay+100
        # fov = 10
        # self.camLens.setFov(fov)

        # scale_y = sin(task.time*5)*2+2
        # scale_y = task.time+1
        scale_y = 1
        self.model.setScale(1, scale_y, 1)

        self.pos = self.cam.getPos()
        self.currents[0] = self.pos[0]
        self.currents[1] = self.pos[1]
        self.currents[2] = self.pos[2]
        self.hpr = self.cam.getHpr()
        self.currents[3] = self.hpr[0]
        self.currents[4] = self.hpr[1]
        self.currents[5] = self.hpr[2]
        self.currents[6] = scale_y
        self.currents[7] = self.camLens.getFov()[0]

        if task.frame < 3:
            self.lasts = self.currents[:]

        for i in range(8):
            self.deltas[i] = self.currents[i] - self.lasts[i]

        self.delta = 0
        for i in range(8):
            self.delta += abs(self.deltas[i]*self.weights[i])

        if self.delta > self.max_delta:
            self.max_delta = self.delta

        # print(self.currents)
        # print(self.max_delta, self.delta)

        # self.filters.setBlurSharpen(0)
        self.filters.setBlurSharpen(1 - self.delta)
        # self.filters.setBlurSharpen(2 - self.delta * 2)

        self.lasts = self.currents[:]
        return Task.cont

app = MyApp()

app.run()
