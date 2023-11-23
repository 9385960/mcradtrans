import matplotlib.pyplot as plt
import numpy as np
#Create and immediately show a sphere
def plot_sphere(r,c,a):
    center_x, center_y, center_z = c  # New center coordinates

    # Create data for the sphere surface with the new center
    theta, phi = np.linspace(0, 2 * np.pi, 100), np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    x = center_x + r * np.sin(phi) * np.cos(theta)
    y = center_y + r * np.sin(phi) * np.sin(theta)
    z = center_z + r * np.cos(phi)

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface of the sphere with the new center
    ax.plot_surface(x, y, z, color='b', alpha=a)

    # Set labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('Surface of a Sphere with New Center')

    # Show plot
    plt.show()
#Add a sphere to an existing plot
def add_sphere_plot(r,c,a,fig,ax):
    center_x, center_y, center_z = c  # New center coordinates

    # Create data for the sphere surface with the new center
    theta, phi = np.linspace(0, 2 * np.pi, 100), np.linspace(0, np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    x = center_x + r * np.sin(phi) * np.cos(theta)
    y = center_y + r * np.sin(phi) * np.sin(theta)
    z = center_z + r * np.cos(phi)

    # Plot the surface of the sphere with the new center
    ax.plot_surface(x, y, z, color='b', alpha=a)
