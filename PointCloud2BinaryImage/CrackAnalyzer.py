import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.morphology import skeletonize
from skimage.measure import label, regionprops
from flask import Flask, request, jsonify, send_file
from io import BytesIO

app = Flask(__name__)


class CrackAnalyzer:
    def __init__(self, pcd_file):
        self.pcd_raw = o3d.io.read_point_cloud(pcd_file, format="ply")
        self.min_bound = self.pcd_raw.get_min_bound()
        self.max_bound = self.pcd_raw.get_max_bound()
        self.points_raw = np.asarray(self.pcd_raw.points)
        self.colors_raw = np.asarray(self.pcd_raw.colors)
        self.center_point = (self.min_bound + self.max_bound) / 2

    def crop_point_cloud(self, click1_x, click1_y, click2_x, click2_y):
        crop_min_bound = [
            min(click1_x, click2_x),
            min(click1_y, click2_y),
            self.min_bound[2],
        ]
        crop_max_bound = [
            max(click1_x, click2_x),
            max(click1_y, click2_y),
            self.max_bound[2],
        ]
        bounding_box = o3d.geometry.AxisAlignedBoundingBox(
            crop_min_bound, crop_max_bound
        )
        self.cropped_pcd = self.pcd_raw.crop(bounding_box)
        o3d.io.write_point_cloud("OverlaySceneCropped.ply", self.cropped_pcd)

    def filter_red_points(self):
        colors = np.asarray(self.cropped_pcd.colors)
        red_mask = (colors[:, 0] > 0.8) & (colors[:, 1] < 0.2) & (colors[:, 2] < 0.2)
        red_points = np.asarray(self.cropped_pcd.points)[red_mask]
        self.red_pcd = o3d.geometry.PointCloud()
        self.red_pcd.points = o3d.utility.Vector3dVector(red_points)
        o3d.io.write_point_cloud("redCloud.ply", self.red_pcd, write_ascii=True)

    def pointcloud_to_binary_image(self, plane="XY", resolution=0.1):
        points = np.asarray(self.red_pcd.points)
        if plane == "XY":
            x, y = points[:, 0], points[:, 1]
        elif plane == "XZ":
            x, y = points[:, 0], points[:, 2]
        elif plane == "YZ":
            x, y = points[:, 1], points[:, 2]
        else:
            raise ValueError("Invalid plane. Choose 'XY', 'XZ', or 'YZ'.")

        if len(x) == 0 or len(y) == 0:
            self.binary_img = np.zeros((1, 1), dtype=np.uint8)
            return

        x_min = np.min(x)
        y_min = np.min(y)
        x -= x_min
        y -= y_min
        x_discrete = (x // resolution).astype(int)
        y_discrete = (y // resolution).astype(int)
        if y_discrete.max() < 0 or x_discrete.max() < 0:
            raise ValueError("Negative dimensions are not allowed.")
        self.binary_img = np.zeros(
            (y_discrete.max() + 1, x_discrete.max() + 1), dtype=np.uint8
        )
        self.binary_img[y_discrete, x_discrete] = 1

    def skeletonize_image(self):
        self.skeleton = skeletonize(self.binary_img)

    def compute_skeleton_length(self):
        labeled_skeleton = label(self.skeleton)
        props = regionprops(labeled_skeleton)
        self.total_length = sum(prop.area for prop in props)

    def save_images(self):
        img_pil = Image.fromarray((self.binary_img * 255).astype(np.uint8))
        img_pil.save("binary_image.png")

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        points = np.asarray(self.red_pcd.points)
        colors = np.asarray(self.red_pcd.colors)
        ax1.scatter(points[:, 0], points[:, 1], c=colors, s=1)
        ax1.set_title("Crack on Selected Point Cloud")
        fig1.savefig("crack_on_selected_point_cloud.png")
        plt.close(fig1)

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.imshow(self.binary_img, cmap="gray")
        ax2.set_title("Binary Image")
        fig2.savefig("binary_image.png")
        plt.close(fig2)

        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)
        ax3.imshow(self.skeleton, cmap="gray")
        ax3.set_title("Skeletonized Image")
        fig3.savefig("skeletonized_image.png")
        plt.close(fig3)


@app.route("/analyze_crack", methods=["GET"])
def analyze_crack():
    click1_x = float(request.args.get("click1_x"))
    click1_y = float(request.args.get("click1_y"))
    click2_x = float(request.args.get("click2_x"))
    click2_y = float(request.args.get("click2_y"))

    analyzer = CrackAnalyzer("../crack.ply")
    analyzer.crop_point_cloud(click1_x, click1_y, click2_x, click2_y)
    analyzer.filter_red_points()
    analyzer.pointcloud_to_binary_image()
    analyzer.skeletonize_image()
    analyzer.compute_skeleton_length()
    analyzer.save_images()

    response_data = {"total_crack_length": analyzer.total_length}

    return jsonify(response_data)


@app.route("/get_image/<image_name>")
def get_image(image_name):
    image_path = f"./{image_name}"
    return send_file(image_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
