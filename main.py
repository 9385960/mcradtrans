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
    print("Main")
    #Get phase function
    func = PhaseFunctions()
    #initialize cloud
    c = Cloud(1,32,4,2.3,density_offset=1)
    #Create inscribed sphere
    s = Sphere(0.5,np.array([0.5,0.5,0.5]))
    #Generate Path
    path = PhotonPath(np.array([1,0,0]),0.001,c,func.GetScatterDirection,s,np.array([0.5,0.5,0.5]),True)

    points = np.asarray(path.GetPath())

    #print path
    print(points)

    x = points[:,0]
    y =points[:,1]
    z = points[:,2]
    
    pplot.plot_path(x,y,z)
    splot.plot_sphere(s.GetRadius(),s.GetCenter(),0.1)

    fig = plt.figure()
    ax = plt.axes(projection ="3d")

    pplot.add_path_plot(x,y,z,fig,ax)
    splot.add_sphere_plot(s.GetRadius(),s.GetCenter(),0.1,fig,ax)
    points = c.GetPoints()
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]
    #ax.scatter3D(x, y, z, color = "green")
    densities = c.GetDensties()
    cube_length = c.GetSideLength()
    divisions = c.GetDivisions()

    cubes = dv.generate_cubes(densities,cube_length,divisions)
    dv.add_cubes_plot(cubes,fig,ax,0.01)
    plt.show()
    return

main()