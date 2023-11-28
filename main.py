import numpy as np
from cloud import Cloud
from photon_propogation import PhotonPath
from sphere import Sphere
from phasefunctions import PhaseFunctions
import path_plot as pplot
import sphere_plot as splot
import matplotlib.pyplot as plt
import density_visualizer as dv
import matplotlib.animation as animation
import image

def main(): 
    
    #The paramters that describe the simulation
    cube_length = 1
    num_points = 32
    power = 4
    fractal_dimension = 2.3
    uniform_density = 1
    g = 0.5
    albedo = 1
    optical_depth = 2
    dl = 0.01
    particle_mass = 1
    divisions = 5

    #Get phase function
    func = PhaseFunctions()
    #Set the g value
    func.Set_g(g)

    #initialize cloud
    c = Cloud(cube_length,num_points,power,fractal_dimension,density_offset=uniform_density,particle_mass=particle_mass,num_divisions=divisions)
    print("Cloud initialized")

    #Create inscribed sphere
    s = Sphere(0.5,np.array([0.5,0.5,0.5]))
    
    #Compute the cross section
    num_points = c.GetNumPointsInsideSphere(s)
    density = num_points*particle_mass/s.GetVolume()+uniform_density
    sigma = optical_depth/(density*s.GetRadius())

    print("Computing path")
    #Generate Path
    path = PhotonPath(np.array([1,0,0]),dl,c,func.GetScatterDirection,s,np.array([0.5,0.5,0.5]),albedo,sigma,True)
    print("Path Computed")

    #Convert the points into a numpy array
    points = np.asarray(path.GetPath())
    
    #print path
    print(points)
    #Gets the x y and z of the path
    x = points[:,0]
    y =points[:,1]
    z = points[:,2]

    #Creates a new figure
    fig = plt.figure()
    ax = plt.axes(projection ="3d")
    #Plots the path
    pplot.add_path_plot(x,y,z,fig,ax)
    #Adds the sphere that the path should be in
    splot.add_sphere_plot(s.GetRadius(),s.GetCenter(),0.1,fig,ax)

    #Gets the density points
    points = c.GetPoints()
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]

    #uncomment if the scatter points should be plotted
    # ax.scatter3D(x, y, z, color = "green")

    #Gets the parameters needed to generate the density plot
    densities = c.GetDensties()
    cube_length = c.GetSideLength()
    divisions = c.GetDivisions()

    #Plots the density
    cubes = dv.generate_cubes(densities,cube_length,divisions)
    dv.add_cubes_plot(cubes,fig,ax,0.01)
    plt.show()

    #Useful Path information
    print()
    print("Weight of path: ",path.GetW())
    print("Ta total: ",path.GetTa())
    print("Distance Traveled: ", path.GetDistTot())

    width = 100
    height = 100

    frame_num = 100

    x = np.linspace(0,cube_length,width)
    y = np.linspace(0,cube_length,height)
    z = cube_length / frame_num

    def compute_images(frame):
        density_im = np.zeros((width,height))
        density_im_interpolated = np.zeros((width,height))
        for i in range(len(x)):
            for j in range(len(y)):
                density_im[i,j] = c.GetDensity(np.array([x[i],y[j],z*frame]))
                density_im_interpolated[i,j] = c.GetDensityInterpolated(np.array([x[i],y[j],z*frame]))
        return density_im, density_im_interpolated
    
    im1,im2 = compute_images(0)

    fig, (ax1,ax2) = plt.subplots(1,2)
    img1 = ax1.imshow(im1,cmap = 'Greys')
    img2 = ax2.imshow(im2,cmap ='Greys')

    def update(frame):
        new_im1, new_im2 = compute_images(frame)
        img1.set_array(new_im1)
        img2.set_array(new_im2)
        return img1,img2
    
    ani = animation.FuncAnimation(fig,update,frames = frame_num,interval = 50, blit = True)

    plt.tight_layout()
    plt.show()
    #print(density_im)
    #print(density_im_interpolated)
        
    width = 100
    height = 100
    photons_per_pixel = 5

    paths = image.compute_paths(photons_per_pixel,width,height,dl,c,func.GetScatterDirection,s,albedo,sigma)
    
    frame_num = 100

    da = .99 / frame_num

    def compute_images(frame):
        im1 = image.paths_to_skymap1(paths,photons_per_pixel,width,height)
        im2 = image.paths_to_skymap2(paths,photons_per_pixel,width,height,s)
        im3 = image.paths_to_skymap1_albedo(paths,photons_per_pixel,width,height,1-da*frame)
        im4 = image.paths_to_skymap2_albedo(paths,photons_per_pixel,width,height,s,1-da*frame)
        return im1,im2,im3,im4
    
    im1,im2,im3,im4 = compute_images(0)

    fig, ax = plt.subplots(2,2)

    ax[0,0].set_title("Skymap 1 albedo = 1")
    ax[0,1].set_title("Skymap 2 albedo = 1")
    ax[1,0].set_title("Skymap 1")
    ax[1,1].set_title("Skymap 2")

    img1 = ax[0,0].imshow(im1,cmap = 'Greys')
    img2 = ax[0,1].imshow(im2,cmap ='Greys')
    img3 = ax[1,0].imshow(im3,cmap = 'Greys')
    img4 = ax[1,1].imshow(im4,cmap = 'Greys')

    def update(frame):
        new_im1, new_im2, new_im3, new_im4 = compute_images(frame)
        img1.set_array(new_im1)
        img2.set_array(new_im2)
        img3.set_array(new_im3)
        img4.set_array(new_im4)
        return img1,img2,img3,img4
    
    ani = animation.FuncAnimation(fig,update,frames = frame_num,interval = 50, blit = True)

    plt.tight_layout()
    plt.show()
    
    return

main()