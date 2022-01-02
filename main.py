from panda3d.core import *
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # print(self.win.getGsg().getSupportsBasicShaders())
        # quit()

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

        # self.point_cloud = self.model.find("**/+GeomNode")
        # self.point_cloud.set_render_mode_thickness(5)  # 5
        # for geom in self.point_cloud.node().modify_geoms():
        #     geom.make_points_in_place()

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
        filters = CommonFilters(self.win, self.cam)
        filters.setBloom(blend=(0.3,0.4,0.3,1.0), mintrigger=0.0, desat=0, intensity=1.0, size="large")  # blend=(0.3,0.4,0.3,0.0), (0.0,0.0,0.0,1.0)
        filters.setCartoonInk()
        # filters.setVolumetricLighting(caster=self.point_cloud, numsamples=64, density=1.0, decay=0.98, exposure=1.0)
        # filters.setInverted()
        filters.setBlurSharpen(0.0)
        # filters.setAmbientOcclusion()
        # filters.setGammaAdjust(1.5)

        self.render.setShaderAuto()

        self.camLens.setFov(100)

        self.wireframeOn()

app = MyApp()
app.run()
