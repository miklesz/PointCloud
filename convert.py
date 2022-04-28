# Standard library imports
from math import sin, cos, radians
import pickle

# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# Constants
K_VERTICES = 1000
# K_VERTICES = int(12419935/1000)
RTAB = False

NAME = 'garden'
ANGLE = -84  # garden: -84

# NAME = 'garden_large'
# ANGLE = 21.5  # garden_large: 21 (trochę leci w prawo), 22 (trochę leci w lewo)

theta = radians(ANGLE)
cos_t = cos(theta)
sin_t = sin(theta)

# Init ShowBase
base = ShowBase()

# Convert
# model_key = 'room_2'
# ext = 'obj'
# model = base.loader.loadModel(f 'models/{model_key}/textured_output.{ext}')
# model = base.loader.loadModel(f 'models/bar_ply.ply')


def create_points():
    global theta, cos_t, sin_t
    # Define GeomVertexArrayFormats for the various vertex attributes.
    array = GeomVertexArrayFormat()
    array.addColumn(InternalName.make("vertex"), 3, Geom.NT_float32, Geom.C_point)
    array.addColumn(InternalName.make("color"), 4, Geom.NT_uint8, Geom.C_color)
    array.addColumn(InternalName.make("index"), 1, Geom.NT_int32, Geom.C_index)

    vertex_format = GeomVertexFormat()
    vertex_format.addArray(array)
    vertex_format = GeomVertexFormat.registerFormat(vertex_format)

    vertex_data = GeomVertexData("point_data", vertex_format, Geom.UH_static)
    # vertex_data.set_num_rows(8)

    pos_writer = GeomVertexWriter(vertex_data, "vertex")
    index_writer = GeomVertexWriter(vertex_data, "index")
    color_writer = GeomVertexWriter(vertex_data, 'color')

    # print('Reading lines')
    # with open(f'models_other/{NAME}.ply') as f:
    #     lines = f.readlines()
    # print(f'Read {len(lines)} lines')
    # skip = lines.index('end_header\n')+1
    # lines = lines[skip:]
    # points = []
    # print('Appending points')
    # for line in lines:
    #     fields = line.split()
    #     x, y, z = float(fields[0]), float(fields[1]), float(fields[2])
    #     if RTAB:
    #         r, g, b, a = float(fields[6])/255, float(fields[7])/255, float(fields[8])/255, 1
    #     else:
    #         r, g, b, a = float(fields[3])/255, float(fields[4])/255, float(fields[5])/255, 1
    #     points.append([x, y, z, r, g, b, a])
    #
    # print('Dumping points')
    # with open(f'{NAME}', 'wb') as f2:
    #     pickle.dump(points, f2)

    print('Loading points')
    with open(f'{NAME}', 'rb') as f2:
        points = pickle.load(f2)

    if theta:
        print('Rotating points')
        for i in range(len(points)):
            points[i][0], points[i][1] = points[i][0]*cos_t-points[i][1]*sin_t, points[i][0]*sin_t+points[i][1]*cos_t

    print('Excluding points (if applicable)')

    # Przedpokój przy WC
    # points = [point for point in points if point[2] < -0.1 and point[0] > 0.2]

    # Schody dolne
    # points = [point for point in points if point[0] <= 0.2 and point[1] > -0.4]
    # points = [point for point in points if not (point[0] > -2.0 and point[2] > -0.1)]

    # Schody górne
    # points = [point for point in points if point[1] <= -0.4 and point[0] < -2.2]

    # Rejestracja
    # points = [point for point in points if point[0] >= -2.2 and point[2] >= -0.1]
    # points = [point for point in points if not (point[0] < -1.8 and point[1] > 0.5 and point[2] < 0.1)]

    # garden_large
    # points = [point for point in points if point[1] < 4]

    # garden
    points = [point for point in points if point[1] >= -8.7]
    # points = [point for point in points if point[1] < -8.7]

    print(f'len(points) = {len(points)}')
    factor = len(points)/(K_VERTICES * 1000)
    print(f'factor = {factor}')

    print('Constructing object')
    for vertex in range(K_VERTICES * 1000):
        x, y, z, r, g, b, a = points[int(vertex*factor)]
        pos_writer.addData3(x, y, z)
        color_writer.addData4(r, g, b, a)
        index_writer.addData1i(vertex)

    # index = 0
    # for line in lines:
    #     fields = line.split()
    #     # print(fields)
    #     x, y, z = float(fields[0]), float(fields[1]), float(fields[2])
    #     if RTAB:
    #         r, g, b, a = float(fields[6])/255, float(fields[7])/255, float(fields[8])/255, 1
    #     else:
    #         r, g, b, a = float(fields[3])/255, float(fields[4])/255, float(fields[5])/255, 1
    #
    #     # print(x, y, z, r, g, b, a)
    #     pos_writer.addData3(x, y, z)
    #     color_writer.addData4(r, g, b, a)
    #     index_writer.addData1i(index)
    #     index += 1

    prim = GeomPoints(Geom.UH_static)
    prim.addNextVertices(K_VERTICES * 1000)  # 8 len(lines)
    # prim.addNextVertices(len(lines))  # 8 len(lines)
    geom = Geom(vertex_data)
    geom.addPrimitive(prim)
    node = GeomNode(f'{NAME}_{K_VERTICES}k')
    node.addGeom(geom)

    return node


# model = base.loader.loadModel(f 'models/bar.bam')
model = base.render.attach_new_node(create_points())
model.setRenderModeThickness(3)
model.reparentTo(base.render)

# Poziomy podłogi
print(model.get_tight_bounds())
# Poziom -.5: -3.1658000
# Poziom 0: -1.1648100
# Poziom +.5: -0.0899634

# Set frame rate meter
base.set_frame_rate_meter(True)

# model.setHpr(0, 90, 0)
# base.run()

model.writeBamFile(f'models/{NAME}_{K_VERTICES}k.bam')
