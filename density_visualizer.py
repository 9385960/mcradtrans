import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

#Function to generate a cube to be visualized
def generate_cube(side_length, bottom_left_front, color='cyan'):
    #Uses the bottom left corner to get position x y and z of the bottom corner
    x, y, z = bottom_left_front

    # Define cube vertices
    cube_definition = [
        [x, y, z], [x + side_length, y, z], [x + side_length, y + side_length, z],
        [x, y + side_length, z], [x, y, z + side_length], [x + side_length, y, z + side_length],
        [x + side_length, y + side_length, z + side_length], [x, y + side_length, z + side_length],
    ]

    # Define cube faces by specifying vertices for each face
    cube_faces = [
        [cube_definition[0], cube_definition[1], cube_definition[2], cube_definition[3]],  # bottom face
        [cube_definition[4], cube_definition[5], cube_definition[6], cube_definition[7]],  # top face
        [cube_definition[0], cube_definition[1], cube_definition[5], cube_definition[4]],  # front face
        [cube_definition[2], cube_definition[3], cube_definition[7], cube_definition[6]],  # back face
        [cube_definition[0], cube_definition[3], cube_definition[7], cube_definition[4]],  # left face
        [cube_definition[1], cube_definition[2], cube_definition[6], cube_definition[5]],  # right face
    ]
    #Returns the cube
    return [cube_definition, cube_faces, color]
#Function to plot cubes with optional data
def plot_cubes(cube_data,additional_data = False,x = [],y = [],z = []):
    #Creates plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #If additional data is to be plotted it will be added here
    if(additional_data):
        ax.scatter3D(x,y,z,color = "green")
    #Goes over every cube in the cube data array
    for cube_definition, cube_faces, color in cube_data:
        # Plotting cube faces and edges with specified color
        cube = Poly3DCollection(cube_faces, alpha=0.1, facecolors=color, edgecolors=color)
        ax.add_collection3d(cube)

    # Automatically adjust axes to include all cubes
    all_verts = [v for cube_def, _, _ in cube_data for v in cube_def]
    max_range = max(max(all_verts))
    min_range = min(min(all_verts))
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)
    
    # Labels plot
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Density Plot')

    plt.show()


def add_cubes_plot(cube_data,fig,ax, a = 0.1):
    #Goes over every cube in the cube data array
    for cube_definition, cube_faces, color in cube_data:
        # Plotting cube faces and edges with specified color
        cube = Poly3DCollection(cube_faces, alpha=a, facecolors=color, edgecolors=color)
        ax.add_collection3d(cube)

    # Automatically adjust axes to include all cubes
    all_verts = [v for cube_def, _, _ in cube_data for v in cube_def]
    max_range = max(max(all_verts))
    min_range = min(min(all_verts))
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)

#A function for generating the density cubes for the plot
def generate_cubes(densities, cube_length, divisions):
    #Gets the largest density value
    biggest_density = np.max(densities)
    #Computes the side length of the box
    sideLength = cube_length/divisions
    #Creates an array to store all the cubes
    cubes = [0]*divisions*divisions*divisions
    #Index to keep track of the cubes created so far
    index = 0
    #loops over every cube and creates a cube in the cubes array
    for i in range(divisions):  
        for j in range(divisions):
            for k in range(divisions):
                bottom_left = [sideLength*i,sideLength*j,sideLength*k]
                normalized_den = densities[i][j][k]/biggest_density
                cubes[index] = generate_cube(sideLength,bottom_left,[normalized_den,normalized_den,normalized_den,normalized_den])
                index += 1
    #returns the cubes created
    return cubes