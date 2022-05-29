# Standard library imports
from math import sin, cos, radians
import pickle

# Related third party imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.filter.CommonFilters import CommonFilters

# Constants
# K_VERTICES = 2000
# K_VERTICES = 1000
K_VERTICES = 200
# NAME = 'stairs_low'
# NAME = 'lead'
# NAME = 'villa_0'
# NAME = 'villa_1'
# NAME = 'villa_2'
# NAME = 'villa_3'
# NAME = 'villa_4'
# NAME = 'nox'
# NAME = 'xenium'
# NAME = 'sitek'
# NAME = 'p1'
# NAME = 'river'
# NAME = 'protracker'
# NAME = 'alco'
# NAME = 'villa_garden'
# NAME = 'villa_street'
# NAME = 'pano'
# NAME = 'spodek'
# NAME = 'party_all'
# NAME = 'party_3some'
# NAME = 'signboard'
RTAB = False

# Init ShowBase
base = ShowBase()

base.setBackgroundColor(1, 0, 0)

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

    # with open(f'models_other/{NAME}.ply') as f:
    #     lines = f.readlines()
    # skip = lines.index('end_header\n')+1
    # lines = lines[skip:]
    # points = []
    # for line in lines:
    #     fields = line.split()
    #     x, y, z = float(fields[0]), float(fields[1]), float(fields[2])
    #     theta = radians(114)
    #     x, y = x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta)
    #     if RTAB:
    #         r, g, b, a = float(fields[6])/255, float(fields[7])/255, float(fields[8])/255, 1
    #     else:
    #         r, g, b, a = float(fields[3])/255, float(fields[4])/255, float(fields[5])/255, 1
    #     points.append([x, y, z, r, g, b, a])

    # with open('points', 'wb') as f2:
    #     pickle.dump(points, f2)

    # with open('points', 'rb') as f2:
    #     points = pickle.load(f2)

    # points = [point for point in points if 0.35 < point[1] < 0.85]
    # new_points = []
    # for point in points:
    #     gray = 0.299 * point[3] + 0.587 * point[4] + 0.114 * point[5]
    #     if 0.38 < point[1] < 0.81 and 0.17 < point[2] < 0.51 and gray > .5:
    #         point[3] = 73/255
    #         point[4] = 92/255
    #         point[5] = 113/255
    #         # point[3] = 91 / 255
    #         # point[4] = 113 / 255
    #         # point[5] = 137 / 255
    #     # else:
    #     new_points.append(point)

    # Read image
    points = []
    my_image = PNMImage(Filename(f'chronicle/{NAME}.png'))
    x_size = my_image.getXSize()
    y_size = my_image.getYSize()
    K_VERTICES = round(x_size * y_size / 7000)
    print(f'K_VERTICES = {K_VERTICES}')


    print(f'x_size = {x_size}, y_size = {y_size}')
    rand = Randomizer()
    for vertex in range(K_VERTICES * 1000):
        im_x = rand.randomInt(x_size)
        im_y = rand.randomInt(y_size)
        # print(im_x, im_y)
        xel_a = my_image.getXelA(im_x, im_y)
        # print(xel_a)
        pos_writer.addData3(
            im_x/1000-x_size/1000/2,
            rand.randomRealUnit()*2*0.01 + ((im_x/1000-x_size/1000/2)/2)**2 + ((-im_y/1000+y_size/1000/2)/2)**2,
            -im_y/1000+y_size/1000/2
        )
        # color_writer.addData4(xel_a[0], xel_a[1], xel_a[2], xel_a[3])
        color_writer.addData4(
            xel_a[0],
            xel_a[1],
            xel_a[2],
            1
        )
        index_writer.addData1i(vertex)


        # x, y, z, r, g, b, a = points[int(vertex*factor)]
        # pos_writer.addData3(x, y, z)
        # color_writer.addData4(r, g, b, a)
        # index_writer.addData1i(vertex)

    # exit()

    # for x in range(my_image.getXSize()):
    #     for y in range(my_image.getYSize()):
    #         xel_a = my_image.getXelA(x, y)
    #         print(xel_a)
    #         gray = 0.299 * xel_a[0] + 0.587 * xel_a[1] + 0.114 * xel_a[2]
            # if gray > .5:
            #     # new_points.append([0, 0.38+x/100 , 0.51-y/100, xel_a[0], xel_a[1], xel_a[2], 1])
            #     # new_points.append([+.1, 0.38 + x / 1000, 0.51 - y / 1000, xel_a[0]/255, 1, 1, 1])
            #     new_points.append([+.07, 0.38+x/380*(.81-.38), 0.51-0.02-+y/380*(.81-.38), xel_a[0], xel_a[1], xel_a[2], 1])

    # points = new_points

    # Schody dolne
    # points = [point for point in points if point[0] < 0.2]

    # print(f'len(points) = {len(points)}')
    # factor = len(points)/(K_VERTICES * 1000)
    # print(f'factor = {factor}')



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
    # node = GeomNode(f'{NAME}_{K_VERTICES}k')
    node = GeomNode(f'{NAME}')
    node.addGeom(geom)

    return node


# model = base.loader.loadModel(f 'models/bar.bam')
model = base.render.attach_new_node(create_points())
model.setRenderModeThickness(10)
model.reparentTo(base.render)
filters = CommonFilters(base.win, base.cam)
filters.set_cartoon_ink(separation=2)

# base.cam.setPosHpr(0, -2, 0, 0, 0, 0)
# base.cam.setPosHpr(0, -3, 0, 0, 0, 0)
# base.cam.setPosHpr(0, 0, 20, 0, -90, 0)
# base.cam.setPosHpr(1.5, .5, .3, 90, 0, 0)

model.setHpr(00, 0, 0)
base.camLens.setFov(90)
base.camLens.setNear(.1)

model.writeBamFile(f'models/{NAME}.bam')
base.run()










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
