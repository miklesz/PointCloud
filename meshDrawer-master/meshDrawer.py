"""
    This example show how to use MeshDrawer to draw
    on the screen in any way shape or form you want
    
    The texture MeshDrawer takes is a plate of
    for instance plate of 3 x 3 will be numberd 
    this way:
     
    1 2 3  
    4 5 6
    7 8 9
    
    The plates are created by the create plate tool 

"""
import direct.directbase.DirectStart

# from pandac.PandaModules import *
from panda3d.core import *

from random import *
from math import *

maxParticles = 20000 # max number of particle (1000) triangles we will display
by = 16 # we have a 16x16 plate texture

generator = MeshDrawer()
generator.setBudget(maxParticles)
# generator.setPlateSize(by)
generatorNode = generator.getRoot()
generatorNode.reparentTo(render)
generatorNode.setDepthWrite(False)
generatorNode.setTransparency(True)
generatorNode.setTwoSided(True)
#generatorNode.setTexture(loader.loadTexture("radarplate.png"))
generatorNode.setBin("fixed",0)
generatorNode.setLightOff(True)

# load some thing into our scene
base.setFrameRateMeter(True)
base.setBackgroundColor(.1,.1,.1,1)
t = loader.loadModel('teapot')
t.reparentTo(render)
t.setPos(0,0,-1)

# base.camera.setZ(-1000)

# very usefull function
def randVec():
    return Vec3(random()-.5,random()-.5,random()-.5)


seed(1988)  # random seed - remove if you always want different random results

# create 100 random particles
particles = []
for i in range(20000):
    #fr = randVec()*100
    #print(type(fr))

    # p = [randVec()*1, fr, randint(181,207),1,Vec4(random(),random(),random(),1)]
    p = [randVec()*1, randVec()*100,randint(181,207),1,Vec4(random(),random(),random(),1)]
    # p = [randVec()*1, randVec()*100, randint(2,3), 1,Vec4(random(),random(),random(),1)]

    # p = [randVec()*1, LVector3f(100,100,100), randint(181,207),1,Vec4(random(),random(),random(),1)]
    # print(randVec()*1)
    particles.append(p)

# create 100 random lines
lines = []
for i in range(100):
    l = [randVec()*100,randVec()*100,187,.1,Vec4(random(),random(),random(),1)]
    lines.append(l)

def drawtask(taks):
    """ this is called every frame to regen the mesh """
    t = globalClock.getFrameTime()
    generator.begin(base.cam,render)
    for v,pos,frame,size,color in particles:
        generator.billboard(pos+v*t,frame,size*sin(t*2)+3,color)
        # generator.billboard(pos+v*t,200,size*sin(t*2)+3,color)
        # generator.billboard(pos+v*t,frame,size*sin(t*2)+3,color)
        # print(frame)
        # generator.billboard(pos+v*t,frame,size*sin(t*2)+3,color)
        # generator.explosion((0,30,0),frame,.1,(1,1,1,1), seed=1988, number=50, distance=t*10)
        # generator.particle(pos,frame,1,(1,1,1,1), rotation=t*10)
        # generator.particle(pos+v*t, frame, 1, color, 0)
        # frame = Vec4(t, t, t**2, t**2)
        # generator.particle(pos, frame, 1, color, 0)
        # generator.blendedParticle(pos, 190, 210, t/10, 1, color, 0)
        # print(frame)
        # quit()

        # print(pos)

    # for start,stop,frame,size,color in lines:
    #     generator.segment(start,stop,frame,size*sin(t*2)+2,color)
    generator.end()
    return taks.cont

# add the draw task to be drawn every frame
taskMgr.add(drawtask, "draw task")

# run the sample
base.run()

