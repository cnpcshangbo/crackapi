import open3d as o3d
import laspy
import numpy as np

# Read the LAS file using laspy
las = laspy.read("file-cropped.las")

# Extract the point cloud data
points = np.vstack((las.x, las.y, las.z)).transpose()
colors = np.vstack((las.red, las.green, las.blue)).transpose() / 255.0

# Create an Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)
# Save the point cloud to a file
output_file = "file-cropped.ply"
o3d.io.write_point_cloud(output_file, pcd)

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd])