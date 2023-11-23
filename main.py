import numpy as np
from cloud import Cloud
from photon_propogation import PhotonPath
from sphere import Sphere
from phasefunctions import PhaseFunctions

def main():
    print("Main")
    #Get phase function
    func = PhaseFunctions()
    #initialize cloud
    c = Cloud(1,10,3,2.3)
    #Create inscribed sphere
    s = Sphere(0.2,np.array([0.5,0.5,0.5]))
    #Generate Path
    path = PhotonPath(np.array([1,0,0]),0.01,c,func.GetScatterDirection,s,s.GetCenter(),True)
    #print path
    print(path.GetPath())
    return

main()