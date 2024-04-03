import open3d as o3d
import numpy as np

def filter_red_points(pcd):
    # 将点云转换为numpy数组
    colors = np.asarray(pcd.colors)

    # 定义红色的条件：R > 0.8, G < 0.2, B < 0.2 （颜色值在0到1之间）
    red_mask = (colors[:, 0] > 0.8) & (colors[:, 1] < 0.2) & (colors[:, 2] < 0.2)

    # 使用此掩码筛选点和颜色
    red_points = np.asarray(pcd.points)[red_mask]
    red_colors = colors[red_mask]

    # 创建新的点云对象
    red_pcd = o3d.geometry.PointCloud()
    red_pcd.points = o3d.utility.Vector3dVector(red_points)
    red_pcd.colors = o3d.utility.Vector3dVector(red_colors)

    return red_pcd

# # 读取点云数据
# pcd = o3d.io.read_point_cloud("scene_dense.ply")
#
# # 筛选红色的点云
# red_pcd = filter_red_points(pcd)
#
# # 保存筛选后的红色点云
# o3d.io.write_point_cloud("redCloud.pcd", red_pcd)
#
# # 可视化筛选后的红色点云
# o3d.visualization.draw_geometries([red_pcd])
