import matplotlib.pyplot as plt
import numpy as np
from plyfile import PlyData
import configparser

# Load the point cloud data from the PLY file
plydata = PlyData.read('../scene_dense_small.ply')

# Extract the vertex data
vertex_data = plydata['vertex']

# Extract the x and y coordinates and the colors
x_coords = vertex_data['x']
y_coords = vertex_data['y']
colors = vertex_data[['red', 'green', 'blue']]
colors_np = np.array(colors.tolist())

# Normalize the colors to the range [0, 1]
normalized_colors = colors_np / 255.0

# Create a scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(x_coords, y_coords, c=normalized_colors, s=1)

# Initialize a list to store click coordinates
click_coords = []

# Define the event handler function
def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        click_coords.append((event.xdata, event.ydata))
        print(f"Clicked at: ({event.xdata}, {event.ydata})")

        # After two clicks, save to config file and disconnect the event handler
        if len(click_coords) == 2:
            config = configparser.ConfigParser()
            config['Clicks'] = {
                'click1_x': str(click_coords[0][0]),
                'click1_y': str(click_coords[0][1]),
                'click2_x': str(click_coords[1][0]),
                'click2_y': str(click_coords[1][1])
            }

            with open('clicks_config.ini', 'w') as configfile:
                config.write(configfile)

            print("Two clicks recorded. Coordinates saved to clicks_config.ini.")
            fig.canvas.mpl_disconnect(cid)

# Connect the event handler to the figure
cid = fig.canvas.mpl_connect('button_press_event', on_click)

# Display the plot
plt.show()
