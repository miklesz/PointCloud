# Standard library imports
from math import sin, cos, radians

# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# Constants
IMAGE_NAMES = ('background', '0', '1', '2', '3', '4', '5', '6')
IMAGE_I = 7
# STEP = 1

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
# for alpha in range(-180, 180, STEP):
#     for beta in range(-90, 90, STEP):
#         x = cos(radians(alpha))*cos(radians(beta))+rand.randomRealUnit()/20
#         y = sin(radians(beta))+rand.randomRealUnit()/20
#         z = sin(radians(alpha))*cos(radians(beta))+rand.randomRealUnit()/20
#         rgba = ((1, 0, 0, .5), (1, 1, 1, .5))[alpha//20 % 2 ^ beta//20 % 2]
#         points.append((x, y, z)+rgba)

image = PNMImage(Filename(f'models_other/mpl/{IMAGE_NAMES[IMAGE_I]}.png'))
x_size = image.getXSize()
y_size = image.getYSize()
print(x_size, y_size)
for y in range(y_size):
    for x in range(x_size):
        xel_a = image.get_xel_a(x, y)
        if xel_a[3] > 0:
            # print(xel_a)
            point_x = rand.randomRealUnit() / 20 + (+x - x_size / 2) / (240 / 1)
            point_y = rand.randomRealUnit() / 20
            point_z = rand.randomRealUnit() / 20 + (-y + y_size / 2) / (240 / 1)
            point = (point_x, point_y, point_z) + tuple(xel_a)
            # print(point)
            points.append(point)

# Constructing object
print('Constructing object')
print(f'len(points) = {len(points)}')
for point in points:
    x, y, z, r, g, b, a = point
    pos_writer.addData3(x, y, z)
    color_writer.addData4(r, g, b, a)

prim = GeomPoints(Geom.UH_static)
prim.addNextVertices(len(points))  # 8 len(lines)
geom = Geom(vertex_data)
geom.addPrimitive(prim)
node = GeomNode(IMAGE_NAMES[IMAGE_I])
node.addGeom(geom)

print('Ready!!!')

# model = base.loader.loadModel(f 'models/bar.bam')
model = base.render.attach_new_node(node)
model.setRenderModeThickness(10)
model.reparentTo(base.render)
model.setTransparency(TransparencyAttrib.M_alpha)

# Poziomy pod??ogi
print(model.get_tight_bounds())

# Set frame rate meter
base.set_frame_rate_meter(True)

# model.setHpr(90, -60, 0)
model.writeBamFile(f'models/{IMAGE_NAMES[IMAGE_I]}.bam')
base.run()
