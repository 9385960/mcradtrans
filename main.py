import numpy as np
from cloud import Cloud
from photon_propogation import PhotonPath
from sphere import Sphere
from phasefunctions import PhaseFunctions
import path_plot as pplot
import sphere_plot as splot
import matplotlib.pyplot as plt
import density_visualizer as dv

def main(): 
    #Get phase function
    func = PhaseFunctions()
    #initialize cloud
    c = Cloud(1,32,4,2.3,density_offset=1)
    #Create inscribed sphere
    s = Sphere(0.5,np.array([0.5,0.5,0.5]))
    #Generate Path
    path = PhotonPath(np.array([1,0,0]),0.001,c,func.GetScatterDirection,s,np.array([0.5,0.5,0.5]),True)
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
    #ax.scatter3D(x, y, z, color = "green")
    #Gets the parameters needed to generate the density plot
    densities = c.GetDensties()
    cube_length = c.GetSideLength()
    divisions = c.GetDivisions()
    #Plots the density
    cubes = dv.generate_cubes(densities,cube_length,divisions)
    dv.add_cubes_plot(cubes,fig,ax,0.01)
    plt.show()
    return

main()