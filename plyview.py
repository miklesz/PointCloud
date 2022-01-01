from open3d import *

cloud = open3d.io.read_point_cloud("models/room.ply")  # Read the point cloud

open3d.visualization.draw_geometries([cloud])  # Visualize the point cloud
