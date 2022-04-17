# if VERBOSE:
#     print('type(point_cloud):', type(point_cloud))
# if VERBOSE:
#     point_cloud.ls()
#     print('base.model.getTightBounds():', point_cloud.getTightBounds())
#     point_cloud.analyze()
# # quit()
#
# del point_cloud
# del model

# def create_points():
#
#     # Define GeomVertexArrayFormats for the various vertex attributes.
#
#     array = GeomVertexArrayFormat()
#     array.add_column(InternalName.make("vertex"), 3, Geom.NT_float32, Geom.C_point)
#     array.add_column(InternalName.make("color"), 4, Geom.NT_uint8, Geom.C_color)
#     array.add_column(InternalName.make("index"), 1, Geom.NT_int32, Geom.C_index)
#
#     vertex_format = GeomVertexFormat()
#     vertex_format.add_array(array)
#     vertex_format = GeomVertexFormat.register_format(vertex_format)
#
#     vertex_data = GeomVertexData("point_data", vertex_format, Geom.UH_static)
#     vertex_data.set_num_rows(8)
#
#     pos_writer = GeomVertexWriter(vertex_data, "vertex")
#     index_writer = GeomVertexWriter(vertex_data, "index")
#
#     index = 0
#
#     # create 8 points as if they were the corner vertices of a cube
#     for z in (-1., 1.):
#         for x, y in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
#             pos_writer.add_data3(x, y, z)
#             index_writer.add_data1i(index)
#             index += 1
#
#     prim = GeomPoints(Geom.UH_static)
#     prim.add_next_vertices(8)
#     geom = Geom(vertex_data)
#     geom.add_primitive(prim)
#     node = GeomNode("points_geom_node")
#     node.add_geom(geom)
#
#     return node
#
# model = base.render.attach_new_node(create_points())
# model.setRenderModeThickness(10)
# model.reparentTo(base.render)

# model.setColorScale(15/255*2, 35/255*2, 71/255*2, 1)
