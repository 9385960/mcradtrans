import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_path(x,y,z):
    lengths = np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the path
    ax.plot(x, y, z, marker='o')

    # Plot arrows between points with calculated lengths
    for i in range(len(x) - 1):
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        dz = z[i + 1] - z[i]
        length = lengths[i]
        ax.quiver(x[i], y[i], z[i], dx, dy, dz, length=length, normalize=True, color='red')

    # Set labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('3D Path with Dynamically Calculated Length Arrows')

    # Show plot
    plt.show()

def add_path_plot(x,y,z,fig,ax):

    lengths = np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)

    # Plot the path
    ax.plot(x, y, z, marker='o')

    # Plot arrows between points with calculated lengths
    for i in range(len(x) - 1):
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        dz = z[i + 1] - z[i]
        length = lengths[i]
        ax.quiver(x[i], y[i], z[i], dx, dy, dz, length=length, normalize=True, color='red')