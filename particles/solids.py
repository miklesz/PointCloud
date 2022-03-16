from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from direct.gui.DirectGui import *
import time
import math
import random, os, sys


class run_me(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)
        # A set of cubes can act as the "ground", define the dimension:
        # Draw them as the ground:
        self.cubeDimensions = Point3(240, 240, 8)
        colourA = LPoint4f(0, 1, 0, 1)
        positionA = Point3(-120, -120, -20)
        self.spawnAGenericCube(colourA, positionA)
        # Draw a few other blocks to show that the particles do notice other objects:

        self.cubeDimensions = Point3(10, 10, 8)
        colourA = LPoint4f(1, 0, 0, 1)
        positionA = Point3(-5, -15, -12)
        self.spawnAGenericCube(colourA, positionA)

        self.cubeDimensions = Point3(10, 10, 8)
        colourA = LPoint4f(1, 0, 0, 1)
        positionA = Point3(5, 15, -12)
        self.spawnAGenericCube(colourA, positionA)

        # Define a dimension for each particle:
        self.snowParticleDimension = 1.5
        # Parameters to periodically spawn new snow particles:
        self.lastSpawnTime = 0
        self.maxSnowParticleCapacity = 300  # 200
        self.numSpawnedParticles = 0
        self.spawnRangePointA = Point3(-50, -40, 70)
        self.spawnRangePointB = Point3(50, 40, 90)
        # Parameters to drift each snow particle:
        self.driftForceRangeXYA = Point2(-2, -4)
        self.driftForceRangeXYB = Point2(8, 10)
        self.driftForceRateChangeRangeXYA = Point2(-0.06, -0.05)
        self.driftForceRateChangeRangeXYB = Point2(0.08, 0.06)
        self.minSnowPosition = Point2(-80, -80)
        self.maxSnowPosition = Point2(80, 80)
        # Parameters to periodically kill the particles that have: landed and have been on the ground past a certain amount of time:
        self.snowParticleRestTime = 4  # 4
        # For the collisions, traverser:
        self.traverser = CollisionTraverser('traverser')
        base.cTrav = self.traverser
        # A collisionHandlerQueue, to deal with modifying the z position of each snow particle:
        self.generalHandlerQueue = CollisionHandlerQueue()
        # The tasks:
        taskMgr.doMethodLater(0.01, self.taskToSpawnSnowParticle, "spawnSnowTask")  # 0.15
        taskMgr.add(self.taskToDriftParticles, 'driftSnowTask')
        taskMgr.add(self.taskToDropAndKillSnow, 'dropKillSnowTask')

    # --These tasks deal with spawning, drifting and killing snow particles:
    # 1.Spawning particles periodically:
    def taskToSpawnSnowParticle(self, task):
        # print(self.numSpawnedParticles)
        if (self.numSpawnedParticles < self.maxSnowParticleCapacity):
            # modify the dimension a bit:
            self.snowParticleDimension = random.uniform(0.5, 1.5)
            newParticle = self.spawnASnowParticle()
            # set a position for it:
            randX = random.uniform(self.spawnRangePointA.x, self.spawnRangePointB.x)
            randY = random.uniform(self.spawnRangePointA.y, self.spawnRangePointB.y)
            randZ = random.uniform(self.spawnRangePointA.z, self.spawnRangePointB.z)
            newParticle.setPos(randX, randY, randZ)
            self.numSpawnedParticles += 1  # 1
        return task.again

    # 2. Applying some simple drift-force in this case:
    def taskToDriftParticles(self, task):
        # First, find the snow particles:
        npCollection = render.findAllMatches("*snowParticleNumber*")
        listNps = npCollection.getPaths()
        for snowParticle in listNps:
            if (not snowParticle.hasPythonTag("hitGround")):
                currentDriftForce = snowParticle.getPythonTag("currentXYDriftForce")
                currentDriftRateOfChange = snowParticle.getPythonTag("currentXYDriftForceRateChange")
                snowParticle.setX(snowParticle, currentDriftForce.x * globalClock.getDt())
                snowParticle.setY(snowParticle, currentDriftForce.y * globalClock.getDt())
                # apply the change if possible:
                useXVector = currentDriftForce.x + currentDriftRateOfChange.x
                useYVector = currentDriftForce.y + currentDriftRateOfChange.y
                # print("X-DRIFT-D: ",useXVector,currentDriftForce.x,self.driftForceRangeXYA.x,self.driftForceRangeXYB.x)

                if (useXVector < self.driftForceRangeXYA.x or useXVector > self.driftForceRangeXYB.x):
                    # change the rate of change for x:
                    startDriftXRateChange = random.uniform(self.driftForceRateChangeRangeXYA.x,
                                                           self.driftForceRateChangeRangeXYB.x)
                    driftXForce = random.uniform(self.driftForceRangeXYA.x, self.driftForceRangeXYB.x)
                    useXVector = driftXForce
                    snowParticle.setPythonTag("currentXYDriftForce", Point2(driftXForce, currentDriftForce.y))
                    snowParticle.setPythonTag("currentXYDriftForceRateChange",
                                              Point2(startDriftXRateChange, currentDriftRateOfChange.y))
                if (useYVector < self.driftForceRangeXYA.y or useYVector > self.driftForceRangeXYB.y):
                    # change the rate of change for y:
                    startDriftYRateChange = random.uniform(self.driftForceRateChangeRangeXYA.y,
                                                           self.driftForceRateChangeRangeXYB.y)
                    driftYForce = random.uniform(self.driftForceRangeXYA.y, self.driftForceRangeXYB.y)
                    useYVector = driftYForce
                    snowParticle.setPythonTag("currentXYDriftForce", Point2(currentDriftForce.x, driftYForce))
                    snowParticle.setPythonTag("currentXYDriftForceRateChange",
                                              Point2(currentDriftRateOfChange.x, startDriftYRateChange))

                snowParticle.setPythonTag("currentXYDriftForce", Point2(useXVector, useYVector))
                if (snowParticle.getX() < self.minSnowPosition.x):
                    snowParticle.setX(self.minSnowPosition.x)
                    # use a positive vector:
                    currentDriftForce.x = self.driftForceRangeXYB.x
                    currentDriftRateOfChange.x = self.driftForceRateChangeRangeXYB.x
                    useXVector = currentDriftForce.x + currentDriftRateOfChange.x
                    snowParticle.setX(snowParticle, useXVector * globalClock.getDt())
                    snowParticle.setPythonTag("currentXYDriftForce", currentDriftForce)
                    snowParticle.setPythonTag("currentXYDriftForceRateChange", currentDriftRateOfChange)
                if (snowParticle.getX() > self.maxSnowPosition.x):
                    snowParticle.setX(self.maxSnowPosition.x)
                    # use a negative vector:
                    currentDriftForce.x = self.driftForceRangeXYA.x
                    currentDriftRateOfChange.x = self.driftForceRateChangeRangeXYA.x
                    useXVector = currentDriftForce.x + currentDriftRateOfChange.x
                    snowParticle.setX(snowParticle, useXVector * globalClock.getDt())
                    snowParticle.setPythonTag("currentXYDriftForce", currentDriftForce)
                    snowParticle.setPythonTag("currentXYDriftForceRateChange", currentDriftRateOfChange)
                if (snowParticle.getY() < self.minSnowPosition.y):
                    snowParticle.setY(self.minSnowPosition.y)
                    # use a positive vector:
                    currentDriftForce.y = self.driftForceRangeXYB.y
                    currentDriftRateOfChange.y = self.driftForceRateChangeRangeXYB.y
                    useYVector = currentDriftForce.y + currentDriftRateOfChange.y
                    snowParticle.setY(snowParticle, useYVector * globalClock.getDt())
                    snowParticle.setPythonTag("currentXYDriftForce", currentDriftForce)
                    snowParticle.setPythonTag("currentXYDriftForceRateChange", currentDriftRateOfChange)
                if (snowParticle.getY() > self.maxSnowPosition.y):
                    snowParticle.setY(self.maxSnowPosition.y)
                    # use a negative vector:
                    currentDriftForce.y = self.driftForceRangeXYA.y
                    currentDriftRateOfChange.y = self.driftForceRateChangeRangeXYA.y
                    useYVector = currentDriftForce.y + currentDriftRateOfChange.y
                    snowParticle.setY(snowParticle, useYVector * globalClock.getDt())
                    snowParticle.setPythonTag("currentXYDriftForce", currentDriftForce)
                    snowParticle.setPythonTag("currentXYDriftForceRateChange", currentDriftRateOfChange)
        return task.cont

    # 3.Lastly, apply some gravity to it, this also implements the kill-cycle:
    def taskToDropAndKillSnow(self, task):
        self.generalHandlerQueue.sortEntries()
        gotHitters = []
        for i in range(self.generalHandlerQueue.getNumEntries()):
            entry = self.generalHandlerQueue.getEntry(i)
            intoNp = entry.getIntoNodePath()
            fromNp = entry.getFromNodePath()
            gotZ = entry.getSurfacePoint(render).getZ()
            actualSnowParticle = fromNp.getParent()
            if (actualSnowParticle not in gotHitters):
                gotHitters.extend([actualSnowParticle, gotZ])
            else:
                gotIndex = gotHitters.index(actualSnowParticle) + 1
                if (gotHitters[gotIndex] < gotZ):
                    gotHitters[gotIndex] = gotZ
        for i in range(0, len(gotHitters), 2):
            actualSnowParticle = gotHitters[i]
            gotZ = gotHitters[i + 1]
            # pull it down:
            if (actualSnowParticle.getZ(render) > gotZ):
                snowGravityAcceleration = actualSnowParticle.getPythonTag("setAcceleration")
                actualSnowParticle.setZ(actualSnowParticle, -snowGravityAcceleration * globalClock.getDt())
            elif (not actualSnowParticle.hasPythonTag("hitGround")):
                actualSnowParticle.setPythonTag("hitGround", globalClock.getFrameTime())
            else:
                timeDiff = globalClock.getFrameTime() - actualSnowParticle.getPythonTag("hitGround")
                if (timeDiff > self.snowParticleRestTime):
                    actualSnowParticle.removeNode()
                    self.numSpawnedParticles -= 1
        return task.cont

    # --End block.

    def spawnASnowParticle(self):
        array = GeomVertexArrayFormat()
        array.addColumn(InternalName.make('vertex'), 3, Geom.NTFloat32, Geom.CPoint)
        array.addColumn(InternalName.make('texcoord'), 2, Geom.NTFloat32, Geom.CTexcoord)
        array.addColumn(InternalName.make('normal'), 3, Geom.NTFloat32, Geom.CNormal)
        array.addColumn(InternalName.make('color'), 4, Geom.NTFloat32, Geom.CColor)
        format = GeomVertexFormat()
        format.addArray(array)
        format = GeomVertexFormat.registerFormat(format)
        node = GeomNode("ASnowFlakeLolz")
        # the writers and geom and primitive:
        vdata = GeomVertexData('VertexData', format, Geom.UHStatic)
        self.PSSTVertex = GeomVertexWriter(vdata, 'vertex')
        self.PSSTNormal = GeomVertexWriter(vdata, 'normal')
        self.PSSTColor = GeomVertexWriter(vdata, 'color')
        self.PSSTTexcoord = GeomVertexWriter(vdata, 'texcoord')
        tileGeom = Geom(vdata)
        tileGeom.setBoundsType(3)
        self.PSSTPrim = GeomTriangles(Geom.UHStatic)
        counter = 0
        snowBody = [0, self.snowParticleDimension, 0, self.snowParticleDimension]
        snowColour = LPoint4f(1, 1, 1, 1)
        self.drawSnowParticle(snowBody, snowColour, counter)
        self.PSSTPrim.closePrimitive()
        tileGeom.addPrimitive(self.PSSTPrim)
        node.addGeom(tileGeom)
        gotProcGeom = render.attachNewNode(node)
        gotProcGeom.setName("snowParticleNumber_" + str(gotProcGeom.node().this))
        # gotProcGeom.setTwoSided(True)
        gotProcGeom.setCollideMask(BitMask32.allOff())
        # attach a collisionRay to it:
        raygeometry = CollisionRay(self.snowParticleDimension / 2, 0, 5, 0, 0, -1)
        groundMask = BitMask32.bit(1)
        snowRay = gotProcGeom.attachNewNode(CollisionNode('NPCavatarRay'))
        snowRay.node().addSolid(raygeometry)
        snowRay.hide()
        # The masks:
        snowRay.node().setIntoCollideMask(BitMask32.allOff())
        snowRay.node().setFromCollideMask(groundMask)
        # add it to the traverser:
        self.traverser.addCollider(snowRay, self.generalHandlerQueue)

        # Lastly, each particle needs to have its own drift-force settings, stored via python-tags:
        startDriftX = random.uniform(self.driftForceRangeXYA.x, self.driftForceRangeXYB.x)
        startDriftY = random.uniform(self.driftForceRangeXYA.y, self.driftForceRangeXYB.y)

        startDriftXRateChange = random.uniform(self.driftForceRateChangeRangeXYA.x, self.driftForceRateChangeRangeXYB.x)
        startDriftYRateChange = random.uniform(self.driftForceRateChangeRangeXYA.y, self.driftForceRateChangeRangeXYB.y)

        gotProcGeom.setPythonTag("currentXYDriftForce", Point2(startDriftX, startDriftY))
        gotProcGeom.setPythonTag("currentXYDriftForceRateChange", Point2(startDriftXRateChange, startDriftYRateChange))
        # also, set the gravity acceleration for it:
        setAcceleration = random.uniform(9, 15)
        gotProcGeom.setPythonTag("setAcceleration", setAcceleration)
        gotProcGeom.setBillboardPointWorld()
        return gotProcGeom

    def drawSnowParticle(self, sentStartEnd, sentColour, counter):
        # sentStartEnd->[xMin,xMax,zMin,zMax]
        # sentColour->[r,g,b,a]
        point1 = Point3(sentStartEnd[0], 0, sentStartEnd[2])
        point2 = Point3(sentStartEnd[1], 0, sentStartEnd[2])
        point3 = Point3(sentStartEnd[1], 0, sentStartEnd[3])
        point4 = Point3(sentStartEnd[0], 0, sentStartEnd[3])
        currentArray = [point1, point2, point3, point4]
        self.drawAGenericFace(self.PSSTVertex, self.PSSTNormal, self.PSSTColor, self.PSSTTexcoord, self.PSSTPrim,
                              counter, currentArray, sentColour)

    def spawnAGenericCube(self, cubeColour, startPoint):
        array = GeomVertexArrayFormat()
        array.addColumn(InternalName.make('vertex'), 3, Geom.NTFloat32, Geom.CPoint)
        array.addColumn(InternalName.make('texcoord'), 2, Geom.NTFloat32, Geom.CTexcoord)
        array.addColumn(InternalName.make('normal'), 3, Geom.NTFloat32, Geom.CNormal)
        array.addColumn(InternalName.make('color'), 4, Geom.NTFloat32, Geom.CColor)
        format = GeomVertexFormat()
        format.addArray(array)
        format = GeomVertexFormat.registerFormat(format)
        node = GeomNode("aCubeGeom")
        # the writers and geom and primitive:
        vdata = GeomVertexData('VertexData', format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')
        tileGeom = Geom(vdata)
        tileGeom.setBoundsType(3)
        prim = GeomTriangles(Geom.UHStatic)
        counter = 0
        genericCubeListPoints = []
        genericCubeListPoints = self.generateCubeGeneric(startPoint, self.cubeDimensions, [])
        for currentArray in genericCubeListPoints:
            self.drawAGenericFace(vertex, normal, color, texcoord, prim, counter, currentArray, cubeColour)
            counter += 4
        prim.closePrimitive()
        tileGeom.addPrimitive(prim)
        node.addGeom(tileGeom)
        gotProcGeom = render.attachNewNode(node)
        gotProcGeom.setName("kyubu_" + str(gotProcGeom.node().this))
        gotProcGeom.setCollideMask(BitMask32.allOff())
        # add a collisionSolid to it:
        endX = startPoint.x + self.cubeDimensions.x
        endY = startPoint.y + self.cubeDimensions.y
        endZ = startPoint.z + self.cubeDimensions.z
        endPoint = Point3(endX, endY, endZ)
        boxSolid = CollisionBox(startPoint, endPoint)
        boxColliderA = gotProcGeom.attachNewNode(CollisionNode('boxCNODE'))
        boxColliderA.setName("boxCollider")
        boxColliderA.node().addSolid(boxSolid)
        boxColliderA.show()
        # The masks:
        boxColliderA.setCollideMask(BitMask32.allOff())
        groundMask = BitMask32.bit(1)
        boxColliderA.node().setIntoCollideMask(groundMask)
        boxColliderA.node().setFromCollideMask(BitMask32.allOff())

    def generateCubeGeneric(self, originPoint, cubeDimension, exemptFaces):
        genericCubeListPoints = []
        for i in range(1, 7, 1):
            if (i not in exemptFaces):
                # draw it:
                gotArray = self.returnProperFaceCoordinates(originPoint, cubeDimension, i)
                genericCubeListPoints.append(gotArray)
        return genericCubeListPoints

    def returnProperFaceCoordinates(self, *args):
        # 0->(xOrigin,yOrigin,zOrigin)
        # 1->(xDimension,yDimension,zDimension)
        # 2->side to draw: 1,2,3,4,5,6: front,back,left,right,top,bottom
        originPoint = args[0]
        dimensionData = args[1]
        sideToDraw = args[2]
        if (sideToDraw == 1):
            # drawing the front:
            point1 = Point3(originPoint.x, originPoint.y, originPoint.z)
            point2 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z)
            point3 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z + dimensionData.z)
            point4 = Point3(originPoint.x, originPoint.y, originPoint.z + dimensionData.z)
        elif (sideToDraw == 2):
            # drawing the back:
            point1 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y, originPoint.z)
            point2 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z)
            point3 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z + dimensionData.z)
            point4 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y,
                            originPoint.z + dimensionData.z)
        elif (sideToDraw == 3):
            # drawing the left:
            point1 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z)
            point2 = Point3(originPoint.x, originPoint.y, originPoint.z)
            point3 = Point3(originPoint.x, originPoint.y, originPoint.z + dimensionData.z)
            point4 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z + dimensionData.z)
        elif (sideToDraw == 4):
            # drawing the right:
            point1 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z)
            point2 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y, originPoint.z)
            point3 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y,
                            originPoint.z + dimensionData.z)
            point4 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z + dimensionData.z)
        elif (sideToDraw == 5):
            # drawing the top:
            point1 = Point3(originPoint.x, originPoint.y, originPoint.z + dimensionData.z)
            point2 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z + dimensionData.z)
            point3 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y,
                            originPoint.z + dimensionData.z)
            point4 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z + dimensionData.z)
        elif (sideToDraw == 6):
            # drawing the bottom:
            point1 = Point3(originPoint.x, originPoint.y + dimensionData.y, originPoint.z)
            point2 = Point3(originPoint.x + dimensionData.x, originPoint.y + dimensionData.y, originPoint.z)
            point3 = Point3(originPoint.x + dimensionData.x, originPoint.y, originPoint.z)
            point4 = Point3(originPoint.x, originPoint.y, originPoint.z)
        return [point1, point2, point3, point4]

    def drawAGenericFace(self, *args):
        # structure is:
        # 0->positional data.
        # 1->normal data.
        # 2->color data.
        # 3->uv data.
        # 4->primitive.
        # 5->current starting index for primitive.
        # 6->face structure.
        # 7->optional colour setting.
        vertex = args[0]
        normal = args[1]
        color = args[2]
        texcoord = args[3]
        prim_dat = args[4]
        numbr = args[5]
        currentArray = args[6]
        for specificPoint in currentArray:
            vertex.addData3f(specificPoint.x, specificPoint.y, specificPoint.z)
            if (len(args) > 7):
                colourData = args[7]
            else:
                colourData = LPoint4f(1, 1, 1, 1)
            color.addData4f(colourData.x, colourData.y, colourData.z, colourData.w)
            texcoord.addData2f(1, 1)
        prim_dat.addVertices(numbr, numbr + 1, numbr + 2)
        prim_dat.addVertices(numbr, numbr + 2, numbr + 3)


runMe = run_me()
runMe.run()