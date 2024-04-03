# This script pops a view to show the binary image and skeletonized image
# Method 1: convert pointCloud to binary image and process the binary image
# Method 2: get skeletonization and measure in 3D
# This file is using the first method
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.morphology import skeletonize
from skimage.measure import label, regionprops

import redFilter
import configparser


def pointcloud_to_binary_image(pcd, plane='XY', resolution=0.01):
    """
    Converts an Open3D PointCloud to a 2D binary image.

    Args:
    - pcd (open3d.geometry.PointCloud): The input point cloud.
    - plane (str): The projection plane ('XY', 'XZ', or 'YZ').
    - resolution (float): The resolution of the grid in the 2D plane.

    Returns:
    - numpy.ndarray: A 2D binary image.
    """

    # Extract the points from the point cloud.
    points = np.asarray(pcd.points)

    if plane == 'XY':
        x, y = points[:, 0], points[:, 1]
    elif plane == 'XZ':
        x, y = points[:, 0], points[:, 2]
    elif plane == 'YZ':
        x, y = points[:, 1], points[:, 2]
    else:
        raise ValueError("Invalid plane. Choose 'XY', 'XZ', or 'YZ'.")

    # Discretize the points.
    x_discrete = (x // resolution).astype(int)
    y_discrete = (y // resolution).astype(int)

    # Create the binary image.
    img = np.zeros((y_discrete.max() + 1, x_discrete.max() + 1), dtype=np.uint8)
    img[y_discrete, x_discrete] = 1

    return img

# Skeletonize the binary image
def skeletonize_image(binary_img):
    return skeletonize(binary_img)

# Compute the length of the skeleton (crack length)
def compute_skeleton_length(skeleton_img):
    labeled_skeleton = label(skeleton_img)
    props = regionprops(labeled_skeleton)

    total_length = sum(prop.area for prop in props)  # summing the area of each segment
    return total_length


# Create a random point cloud for testing purposes.
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(np.random.rand(1000, 3))

pcd_raw = o3d.io.read_point_cloud("../crack.las", format="las")

# Get the minimum and maximum bounds
min_bound = pcd_raw.get_min_bound()
max_bound = pcd_raw.get_max_bound()

print(f"Min bound: {min_bound}")
print(f"Max bound: {max_bound}")

# 提取点云数据
points_raw = np.asarray(pcd_raw.points)
colors_raw = np.asarray(pcd_raw.colors)

center_point = (min_bound + max_bound) / 2

print(f"Center point: {center_point}")

# crop_min_bound = [0.08817603, 0.10874449, 0.98011023] #downside
#
# crop_max_bound = [0.11819754, 0.14, 0.99] #downside

# crop_max_bound[0] = (crop_min_bound[0] + crop_max_bound[0])/2 #left
#
# # crop_min_bound[0] = (crop_min_bound[0] + crop_max_bound[0])/2 # right
#
# crop_min_bound[1] = 0.14 #upside
# crop_max_bound[1] = 0.16 #upside

# Read configuration file
config = configparser.ConfigParser()
config.read('clicks_config.ini')

# Extract the click coordinates
click1_x = float(config['Clicks']['click1_x'])
click1_y = float(config['Clicks']['click1_y'])
click2_x = float(config['Clicks']['click2_x'])
click2_y = float(config['Clicks']['click2_y'])

# Calculate the cropping bounds
crop_min_bound = [min(click1_x, click2_x), min(click1_y, click2_y), min_bound[2]]  # Z-coordinate is set to 0 as a placeholder
crop_max_bound = [max(click1_x, click2_x), max(click1_y, click2_y), max_bound[2]]  # Z-coordinate is set to 0 as a placeholder


# Create the bounding box
bounding_box = o3d.geometry.AxisAlignedBoundingBox(crop_min_bound, crop_max_bound)

OverlaySceneCropped_pcd = pcd_raw.crop(bounding_box)
# 保存筛选后的红色点云
o3d.io.write_point_cloud("OverlaySceneCropped.ply", OverlaySceneCropped_pcd)

# Get the minimum and maximum bounds
OverlaySceneMin_bound = OverlaySceneCropped_pcd.get_min_bound()
OverlaySceneMax_bound = OverlaySceneCropped_pcd.get_max_bound()

print(f"OverlaySceneCroppedMin bound: {OverlaySceneMin_bound}")
print(f"OverlaySceneCroppedMax bound: {OverlaySceneMax_bound}")

# 提取点云数据
OverlayScenePoints_raw = np.asarray(OverlaySceneCropped_pcd.points)
OverlaySceneColors_raw = np.asarray(OverlaySceneCropped_pcd.colors)


# Load the point cloud
# pcd = o3d.io.read_point_cloud("../redCropped.pcd")
# import ../main
pcd = redFilter.filter_red_points(OverlaySceneCropped_pcd)

# 提取点云数据
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)

# 创建Matplotlib图形
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# Convert the point cloud to a binary image.
img = pointcloud_to_binary_image(pcd, plane='XY', resolution=0.001)

# Display the image using Open3D.
# o3d.visualization.draw_geometries([o3d.geometry.Image((img * 255).astype(np.uint8))])

# Display the image using matplotlib.
# plt.imshow(img, cmap='gray')
# plt.axis('off')
# plt.show()

# Save the binary image using PIL.
img_pil = Image.fromarray((img * 255).astype(np.uint8))
img_pil.save('binary_image.png')

# Perform skeletonization
skeleton = skeletonize_image(img)

# Compute the crack length
crack_length = compute_skeleton_length(skeleton)
print(f"Total Crack Length: {crack_length}")

# Display the images
fig, ax = plt.subplots(2, 3, figsize=(10, 5))

ax[0,0].scatter(points_raw[:, 0], points_raw[:, 1], points_raw[:, 2], c=colors_raw)
# ax[0,0].axis('off')
ax[0,0].set_title('Original Point Cloud')
# 2. Add a green rectangle to cover the top-left quarter
axes = ax[0,0]
x_lim = axes.get_xlim()
y_lim = axes.get_ylim()

# x_lim[0] = crop_min_bound[0]

# width = (x_lim[1] - x_lim[0]) / 2
# height = (y_lim[1] - y_lim[0]) / 2
width = crop_max_bound[0] - crop_min_bound[0]
height = crop_max_bound[1] - crop_min_bound[1]

# Create the rectangle starting from the top-left
rect = plt.Rectangle((crop_min_bound[0], crop_min_bound[1]), width, height, facecolor='green', alpha = 0.5)
axes.add_patch(rect)

# plt.show()

# ax[0,1].imshow(OverlaySceneCropped_pcd, cmap='gray')
ax[0,1].scatter(OverlayScenePoints_raw[:, 0], OverlayScenePoints_raw[:, 1], OverlayScenePoints_raw[:, 2], c=OverlaySceneColors_raw)
# ax[0,1].axis('off')
ax[0,1].set_title('Selected Point Cloud')

# 绘制点云
# ax[0,2] = fig.add_subplot(111, projection='3d')
ax[0,2].scatter(points[:, 0], points[:, 1], points[:, 2], c=colors)
# ax[0,2].axis('off')
ax[0,2].set_title('Crack on Selected Point Cloud')


ax[1,0].imshow(img, cmap='gray')
# ax[1,0].axis('off')
ax[1,0].set_title('Binary Image')

ax[1,1].imshow(skeleton, cmap='gray')
# ax[1,1].axis('off')
ax[1,1].set_title('Skeletonized Image')

ax[1,2].axis('off')
ax[1,2].set_title(f"Total Crack Length: {crack_length}")

plt.tight_layout()
plt.show()
#%%
