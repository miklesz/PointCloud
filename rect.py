# from panda3d.core import *
# from direct.showbase.ShowBase import ShowBase
# base = ShowBase()
#
# base.run()

# Source: https://discourse.panda3d.org/t/procedurally-generating-3d-models/14623/2

import sys
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Move camera for a better view
        self.disableMouse() # if you leave mouse mode enabled camera position will be governed by Panda mouse control
        self.camera.setY(-5)

        # Enable fast exit
        self.accept("escape", sys.exit)

        # Create cube
        gNode = self.createCube()
        self.cubeNodePath = self.render.attachNewNode(gNode)

        self.cubeNodePath.setTransparency(TransparencyAttrib.M_alpha)

        # tex = self.loader.loadTexture('maps/noise.rgb')
        # tex = self.loader.loadTexture('chronicle/alco.jpg')
        # tex = self.loader.loadTexture('chronicle/nox.png')
        # tex = self.loader.loadTexture('chronicle/Lenna_(test_image).png')
        # tex = self.loader.loadTexture('chronicle/4-grunge-square-frame-2.png')
        tex = self.loader.loadTexture('chronicle/Neon-Square-PNG-Clipart.png')
        # tex = self.loader.loadTexture('chronicle/alco.png')
        self.cubeNodePath.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.cubeNodePath.setTexTransform(TextureStage.getDefault(), TransformState.makeHpr(LVecBase3f(0, -90, 0)))
        self.cubeNodePath.setTexOffset(TextureStage.getDefault(), .5, .5)
        self.cubeNodePath.setTexScale(TextureStage.getDefault(), .5, 1, .5)
        self.cubeNodePath.setTexProjector(TextureStage.getDefault(), self.render, self.cubeNodePath)
        self.cubeNodePath.setTexture(tex)

        # self.smiley = self.loader.loadModel('smiley.egg')
        # self.smiley.reparentTo(self.render)
        # self.smiley.setTexture(tex, 1)

        # # Add a simple point light
        # plight = PointLight('plight')
        # plight.setColor(VBase4(1, 1, 1, 1))
        # #plight.setAttenuation(Point3(0, 0, 0.5))
        # plnp = self.render.attachNewNode(plight)
        # plnp.setPos(4, -4, 4)
        # self.render.setLight(plnp)
        # # Add an ambient light
        # alight = AmbientLight('alight')
        # alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        # alnp = self.render.attachNewNode(alight)
        # self.render.setLight(alnp)

        # Add the spinCubeTask procedure to the task manager.
        self.taskMgr.add(self.spinCubeTask, "spinCubeTask")

    def spinCubeTask(self, task):
        angleDegrees = task.time * 6.0
        # self.cubeNodePath.setHpr(angleDegrees, angleDegrees, angleDegrees)
        self.cubeNodePath.setHpr(0, 0, angleDegrees)
        return Task.cont

    def createCube(self):
        format = GeomVertexFormat.getV3n3c4()
        vertexData = GeomVertexData('cube', format, Geom.UHStatic)

        vertexData.setNumRows(4)

        vertices = GeomVertexWriter(vertexData, 'vertex')
        # normals = GeomVertexWriter(vertexData, 'normal')
        # colors = GeomVertexWriter(vertexData, 'color')

        vertices.addData3f(-1, 0, 1)
        vertices.addData3f(1, 0, 1)
        vertices.addData3f(1, 0, -1)
        vertices.addData3f(-1, 0, -1)

        # normals.addData3f(0, -1, 0)
        # normals.addData3f(-1, 0, 0)
        # normals.addData3f(0, 0, -1)
        # normals.addData3f(0, -1, 0)

        # colors.addData4f(0, 0, 1, 1)
        # colors.addData4f(0, 1, 0, 1)
        # colors.addData4f(0, 1, 1, 1)
        # colors.addData4f(1, 0, 0, 1)

        # Store the triangles, counter clockwise from front
        primitive = GeomTriangles(Geom.UHStatic)

        primitive.addVertices(3, 1, 0)
        primitive.addVertices(3, 2, 1)

        geom = Geom(vertexData)
        geom.addPrimitive(primitive)

        node = GeomNode('cube gnode')
        node.addGeom(geom)
        return node

app = MyApp()
app.run()