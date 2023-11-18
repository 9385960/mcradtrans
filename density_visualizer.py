import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generate_cube(side_length, bottom_left_front, color='cyan'):
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

    return [cube_definition, cube_faces, color]

def plot_cubes(cube_data,additional_data = False,x = [],y = [],z = []):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    if(additional_data):
        ax.scatter3D(x,y,z,color = "green")

    for cube_definition, cube_faces, color in cube_data:
        # Plotting cube faces and edges with specified color
        cube = Poly3DCollection(cube_faces, alpha=color[-1], facecolors=color, edgecolors=color)
        ax.add_collection3d(cube)

    # Automatically adjust axes to include all cubes
    all_verts = [v for cube_def, _, _ in cube_data for v in cube_def]
    max_range = max(max(all_verts))
    min_range = min(min(all_verts))
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)
    
    # Customize plot
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Cubes with Faces and Edges')

    plt.show()

# Example usage
#side_length = 3
#cubes = [
#    generate_cube(side_length, [2, 2, 2], [0.2,0.2,0.2,0.1]),   # Cube 1 with cyan color
#    generate_cube(side_length, [5, 5, 5], 'magenta')  # Cube 2 with magenta color
#    # Add more cubes here with colors if needed
#]
#plot_cubes(cubes)