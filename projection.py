import laspy
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata  # Import griddata


# Load your LAS file
input_file = laspy.read("file-cropped.las") 

# Extract the relevant points
x = input_file.x
y = input_file.y
z = input_file.z  # Assuming you want to project the Z values
print(x)

# Optional - Scaling for better visualization
scale_factor = 1  # Adjust if needed 
x = x / scale_factor
y = y / scale_factor

# Create a grid for rasterization
grid_size = 0.01  # Adjust the resolution as needed
x_min, x_max = np.min(x), np.max(x)
y_min, y_max = np.min(y), np.max(y)

xi = np.linspace(x_min, x_max, int((x_max - x_min) / grid_size))
yi = np.linspace(y_min, y_max, int((y_max - y_min) / grid_size))
xi, yi = np.meshgrid(xi, yi)

# Interpolation (Choose a method suitable for your data)
zi = griddata((x, y), z, (xi, yi), method='nearest') 

# Create and plot the image
plt.imshow(zi, cmap='gray', extent=[x_min, x_max, y_min, y_max]) 
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Projected Point Cloud Image')
# Save the image
plt.savefig("output_image.png")  # Specify your desired filename and extension

# Optional: Uncomment the following line if you want to display it as well
# plt.show()
