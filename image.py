import numpy as np
from photon_propogation import PhotonPath

# File to create

#Will compute an image at a specific camera position
def compute_image(camera_position, view_direction, num_photons, width, height,up_v, fov,dl,cloud,scatter,sphere,albedo,sigma):
    #photons = np.zeros((width,height,num_photons))
    image = np.zeros((width,height))

    # Calculate aspect ratio
    aspect_ratio = width / height

    # Calculate viewing direction, right vector, and up vector
    viewing_direction = normalize(view_direction)
    right = np.cross(viewing_direction, up_v)
    right = normalize(right)
    up = np.cross(right, viewing_direction)

    # Construct the camera-to-world transformation matrix
    camera_matrix = np.stack((right, up, -viewing_direction)).T

    # Iterate over each pixel in the image
    for i in range(height):
        for j in range(width):
            # Calculate normalized device coordinates (-1 to 1)
            ndc_x = (2 * (j + 0.5) / width - 1) * aspect_ratio * np.tan(np.radians(fov / 2))
            ndc_y = (1 - 2 * (i + 0.5) / height) * np.tan(np.radians(fov / 2))
            
            # Calculate ray direction in camera space
            ray_dir_cam = right * ndc_x + up * ndc_y + viewing_direction
            # Transform ray direction to world space by multiplying with the camera-to-world matrix
            ray_dir_world = normalize(camera_matrix @ ray_dir_cam)
            for k in range(num_photons):
                photon  = PhotonPath(ray_dir_world.copy(),dl,cloud,scatter,sphere,camera_position.copy(),albedo,sigma)
                #photons[i][j][k] = photon
                intensity = np.exp(-photon.GetTsTot())
                image[i][j] += intensity
            image[i][j] = image[i][j]/num_photons
            
    return image
            

    # At this point, ray_directions[i, j] contains the direction of the ray for pixel (i, j)

    
    
    
    return

def compute_pixel_direction(i,j,look_dir,width,height,aspect,up,right):
    
    return normalize(look_dir + (2*j/width-1)*aspect*right + (2*i/height-1)*up)

def normalize(vector):
    
    return vector/get_magnitude(vector)

def get_magnitude(v):
        num = 0
        for i in range(len(v)):
            num += v[i]**2
        return np.sqrt(num)  