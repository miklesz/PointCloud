# Standard library imports
from math import sin, cos, radians

# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# Constants
STEP = 1

# Init ShowBase
base = ShowBase()

# Define GeomVertexArrayFormats for the various vertex attributes.
array = GeomVertexArrayFormat()
array.addColumn(InternalName.make("vertex"), 3, Geom.NT_float32, Geom.C_point)
array.addColumn(InternalName.make("color"), 4, Geom.NT_uint8, Geom.C_color)

vertex_format = GeomVertexFormat()
vertex_format.addArray(array)
vertex_format = GeomVertexFormat.registerFormat(vertex_format)

vertex_data = GeomVertexData("point_data", vertex_format, Geom.UH_static)
# vertex_data.set_num_rows(8)

pos_writer = GeomVertexWriter(vertex_data, "vertex")
color_writer = GeomVertexWriter(vertex_data, 'color')

# Constructing points
print('Constructing points')
points = []
rand = Randomizer()
for alpha in range(-180, 180, STEP):
    for beta in range(-90, 90, STEP):
        x = cos(radians(alpha))*cos(radians(beta))+rand.randomRealUnit()/20
        y = sin(radians(beta))+rand.randomRealUnit()/20
        z = sin(radians(alpha))*cos(radians(beta))+rand.randomRealUnit()/20
        rgba = ((1, 0, 0, .5), (1, 1, 1, .5))[alpha//20 % 2 ^ beta//20 % 2]
        points.append((x, y, z)+rgba)

# Constructing object

print('Constructing object')
print(f'len(points) = {len(points)}')
for point in points:
    x, y, z, r, g, b, a = point
    pos_writer.addData3(x, y, z)
    color_writer.addData4(r, g, b, a)


prim = GeomPoints(Geom.UH_static)
# prim.addNextVertices(K_VERTICES * 1000)  # 8 len(lines)
prim.addNextVertices(len(points))  # 8 len(lines)
geom = Geom(vertex_data)
geom.addPrimitive(prim)
node = GeomNode('ball')
node.addGeom(geom)

print('Ready!!!')

# model = base.loader.loadModel(f 'models/bar.bam')
model = base.render.attach_new_node(node)
model.setRenderModeThickness(10)
model.reparentTo(base.render)
model.setTransparency(TransparencyAttrib.M_alpha)

# Poziomy podłogi
print(model.get_tight_bounds())

# Set frame rate meter
base.set_frame_rate_meter(True)

model.setHpr(90, -60, 0)
# model.writeBamFile('models/ball.bam')
base.run()
