# Standard library imports
from math import sin, cos, radians
import pickle

# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# Constants
K_VERTICES = 200
NAME = 'room_1'
RTAB = False

# Init ShowBase
base = ShowBase()

# Convert
# model_key = 'room_2'
# ext = 'obj'
# model = base.loader.loadModel(f 'models/{model_key}/textured_output.{ext}')
# model = base.loader.loadModel(f 'models/bar_ply.ply')


def create_points():
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

    with open(f'models_other/{NAME}.ply') as f:
        lines = f.readlines()
    skip = lines.index('end_header\n')+1
    lines = lines[skip:]
    points = []
    for line in lines:
        fields = line.split()
        x, y, z = float(fields[0]), float(fields[1]), float(fields[2])
        theta = radians(-169)
        x, y = x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta)
        if RTAB:
            r, g, b, a = float(fields[6])/255, float(fields[7])/255, float(fields[8])/255, 1
        else:
            r, g, b, a = float(fields[3])/255, float(fields[4])/255, float(fields[5])/255, 1
        points.append([x, y, z, r, g, b, a])

    # with open('points', 'wb') as f2:
    #     pickle.dump(points, f2)

    # with open('points', 'rb') as f2:
    #     points = pickle.load(f2)

    # Przedpokój przy WC
    # points = [point for point in points if point[2] < -0.1 and point[0] > 0.2]

    print(f'len(points) = {len(points)}')
    factor = len(points)/(K_VERTICES * 1000)
    print(f'factor = {factor}')

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
model.setRenderModeThickness(5)
model.reparentTo(base.render)
# base.cam.setPosHpr(0, 0, 20, 0, -90, 0)
# base.cam.setPosHpr(0, 0, 0, 180, 0, 0)

# base.run()
model.writeBamFile(f'models/{NAME}_{K_VERTICES}k.bam')

# model.ls()
# model.analyze()

# point_cloud = model.find("**/+GeomNode")
# for geom in point_cloud.node().modify_geoms():
#     geom.make_points_in_place()

# for c in model.findAllMatches("**/+GeomNode"):
#     gn = c.node()
#     for i in range(gn.getNumGeoms()):
#         state = gn.getGeomState(i)
#         state = state.removeAttrib(TextureAttrib.getClassType())
#         gn.setGeomState(i, state)

# do some fancy calculations on the normals, or texture coordinates that you
# don't want to do at runtime

# Save your new custom Panda
# model.writeBamFile(f 'models/{model_key}.bam')

# point_cloud = model_dict[model_key]['model'].find("**/+GeomNode")
# for geom in point_cloud.node().modify_geoms():
#     print(geom)
#     geom.make_points_in_place()
# point_cloud.reparentTo(base.render)
# del model_dict[model_key]['model']
# del point_cloud
#
# model_dict[model_key]['cloud'] = model_dict[model_key]['model'].find("**/+GeomNode")
# for geom in model_dict[model_key]['cloud'].node().modify_geoms():
#     geom.make_points_in_place()

# point_cloud.writeBamFile(f 'models/{model_key}/textured_output.bam')
# point_cloud.writeBamFile(f 'models/bar_ply/textured_output.bam')
# model.writeBamFile(f 'models/bar.bam')
