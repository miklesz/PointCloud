from open3d import *

# cloud = open3d.io.read_point_cloud("models/room.ply")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/220101-221614-Mesh.ply")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01-2.ply")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01.ply")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01.e57")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01.stl")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01.csv")  # Read the point cloud
# cloud = open3d.io.read_point_cloud("models/Modelar-2022-Jan-01.csv")  # Read the point cloud


open3d.visualization.draw_geometries([cloud])  # Visualize the point cloud
