import numpy as np
from photon_propogation import PhotonPath

# File to create

#Will compute an image at a specific camera position
def compute_image(camera_position, view_direction, num_photons, width, height,up_v, fov,dl,cloud,scatter,sphere,albedo,sigma):
    photons = np.empty((width,height,num_photons),dtype=PhotonPath)
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
                photons[i][j][k] = photon
                intensity = np.exp(-photon.GetTsTot())
                image[i][j] += intensity
            image[i][j] = image[i][j]/num_photons
            
    return (image,photon)

#Will compute an image at a specific camera position
def compute_skymap1(num_photons, width, height,dl,cloud,scatter,sphere,albedo,sigma):
    photons = np.empty((width,height,num_photons),dtype=PhotonPath)
    image = np.zeros((width,height))

    # Calculate viewing direction, right vector, and up vector
    thetas = np.linspace(0,np.pi,width)
    phis = np.linspace(0,2*np.pi,height)    

    # Iterate over each pixel in the image
    for i in range(height):
        for j in range(width): 
            x = np.sin(thetas[j])*np.cos(phis[i])
            y = np.sin(thetas[j])*np.sin(phis[i])
            z = np.cos(thetas[j])
            # Calculate ray direction in camera space
            ray_dir = np.array([x,y,z])
            for k in range(num_photons):
                photon  = PhotonPath(ray_dir.copy(),dl,cloud,scatter,sphere,sphere.GetCenter().copy(),albedo,sigma)
                photons[i][j][k] = photon
                intensity = np.exp(-photon.GetTsTot())
                image[i][j] += intensity
            image[i][j] = image[i][j]/num_photons
            
    return (image,photon)

def normalize(vector):
    
    return vector/get_magnitude(vector)

def get_magnitude(v):
        num = 0
        for i in range(len(v)):
            num += v[i]**2
        return np.sqrt(num) 

def rectangular_to_spherical(point):
    x, y, z = point[0], point[1], point[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    
    # Adjust phi to be in the range [0, 2*pi]
    phi = np.where(phi < 0, phi + 2 * np.pi, phi)
    
    return np.array([r, theta, phi])

#Will compute an image at a specific camera position
def compute_skymap2(num_photons, width, height,dl,cloud,scatter,sphere,albedo,sigma):
    photons = np.empty((width,height,num_photons),dtype=PhotonPath)
    image = np.zeros((width,height))

    # Calculate viewing direction, right vector, and up vector
    thetas = np.linspace(0,np.pi,width)
    phis = np.linspace(0,2*np.pi,height)    

    # Iterate over each pixel in the image
    for i in range(height):
        for j in range(width): 
            x = np.sin(thetas[j])*np.cos(phis[i])
            y = np.sin(thetas[j])*np.sin(phis[i])
            z = np.cos(thetas[j])
            # Calculate ray direction in camera space
            ray_dir = np.array([x,y,z])
            for k in range(num_photons):
                photon  = PhotonPath(ray_dir.copy(),dl,cloud,scatter,sphere,sphere.GetCenter().copy(),albedo,sigma)
                photons[i][j][k] = photon
                end_location = photon.GetEndPos()
                end_location = end_location - sphere.GetCenter()
                end_location = rectangular_to_spherical(end_location)
                theta = end_location[1]
                phi = end_location[2]
                dtheta = np.pi/width
                dphi = 2*np.pi/height
                y_index = (int)(np.floor(phi/dphi))
                x_index = (int)(np.floor(theta/dtheta))
                image[y_index][x_index] += 1
            
    return (image,photon)