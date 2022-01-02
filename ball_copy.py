from panda3d.core import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from math import sin, pi

# Filters
from direct.filter.CommonFilters import CommonFilters

# Egg
# from panda3d.egg import EggPolygon, EggVertexPool, EggData, EggVertex, loadEggData, EggCoordinateSystem

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        print(self.win.getGsg().getSupportsBasicShaders())
        quit()

        # Setting background color
        self.setBackgroundColor(0, 0, 0)

        # Loading ball model: https://3dwarehouse.sketchup.com/model/5d3d3a486e9e36d1d736d7e8633a1746/Amiga-boing-ball
        self.model = self.loader.loadModel("ball.dae")

        # Mayo
        # self.model = self.loader.loadModel("mayonnaise_1000ml/scene.gltf")
        # self.model.setScale(0.3)

        self.model.reparentTo(self.render)

        # Fixing bounds
        # self.model.showTightBounds()
        box = self.model.getTightBounds()
        print(box)
        self.model.setPos(-(box[0][0]+box[1][0])/2, -(box[0][1]+box[1][1])/2, -(box[0][2]+box[1][2])/2)
        print(self.model.getTightBounds())
        self.ball = self.render.attachNewNode("ball")
        self.model.reparentTo(self.ball)
        self.ball.reparentTo(self.render)

        # Better Y position (15..20)
        self.ball.setY(17.5)

        # # Spot light
        # spotlight = Spotlight('spotlight')
        # self.spot = self.render.attachNewNode(spotlight)
        # self.spot.setPos(-25, -15, 30)   # -27.4554, -16.2955, 33.2832
        # self.spot.lookAt(self.ball)
        # self.render.setLight(self.spot)
        #
        # # Ambient light
        # ambientlight = AmbientLight('ambient light')
        # ambientlight.setColor((0.1, 0.1, 0.1, 1))
        # self.ambient = self.render.attachNewNode(ambientlight)
        # self.render.setLight(self.ambient)

        # Better rotation
        self.ball.setHpr(90, -60, 0)  # self.ball.setHpr(0, -30, 0)

        # # Loading grid cube model: https://skfb.ly/LDEH
        # self.grid = self.loader.load_model("the_grid/scene.gltf")
        # self.grid.reparentTo(self.render)
        #
        # # Setting scale
        # print(self.grid.getTightBounds())
        # self.grid.setScale(.005)
        # print(self.grid.getTightBounds())
        #
        # # Setting Y position
        # self.grid.setY(2)
        #
        # # Setting Z position
        # self.grid.setZ(15)
        #
        # # Setting X position
        # self.grid.setX(-18.2954/2)
        #
        # # Checking grid position
        # print(self.grid.getTightBounds())

        # Setting shaders
        #self.spot.node().setShadowCaster(True)
        #self.render.setShaderAuto()

        # Fixing shaders - setting depth offset
        # self.render.setDepthOffset(-3)

        # Fixing shaders - adjusting shadow caster
        #self.spot.node().setShadowCaster(True, 8192, 8192)

        # Setting frame rate meter
        self.setFrameRateMeter(True)

        # Rotating
        # self.taskMgr.add(self.spin, "SpinTask")

        # Fog
        # fog = Fog("fog")
        # fog.setColor(.5, .5, .5)
        # fog.setExpDensity(0.1)
        # self.render.setFog(fog)

        # self.cloud = self.loader.loadModel("pokoj.dae")
        # self.cloud.reparentTo(self.render)
        # self.cloud.showTightBounds()
        # print(self.cloud.getTightBounds())

        # Filters
        print(self.win.getGsg().getSupportsBasicShaders())
        filters = CommonFilters(self.win, self.cam)
        # filters.setBloom()
        # filters.setCartoonInk()
        # filters.setVolumetricLighting(self.ball)
        filters.setInverted()
        # filters.setBlurSharpen(2.0)
        # filters.setAmbientOcclusion()
        # filters.setGammaAdjust(1.5)

        # self.ball.writeEgg("ball_w.egg")

        #self.camLens.setFov(100)

    def spin(self, task):

        # Simple spin
        # angle = task.time*72
        # self.ball.setR(angle)

        # Enabling direction
        direction = int(task.time//2.5) % 2
        angle = task.time*72*(direction*2-1)
        self.ball.setR(angle)   # Mayo: self.ball.setH(angle)

        # Shaking (X position)
        if direction:
            x = task.time % 2.5*4-5
        else:
            x = 5-task.time % 2.5*4
        self.ball.setX(x)

        # Bouncing (Z position)
        z = sin(task.time*2 % pi)*4.7-(3.30781-1.60243)
        self.ball.setZ(z)

        # Fov (experimenting)
        # self.camLens.setFov(x*10+30)

        return Task.cont


app = MyApp()
app.run()
