import numpy as np
#Sphere class
class Sphere:
    #Initializes the radius and center
    def __init__(self,r,c):
        self.r = r
        self.c = c
        return
    #Gets the radius
    def GetRadius(self):
        return self.r
    #Gets the center
    def GetCenter(self):
        return self.c
    #Gets the volume of the sphere
    def GetVolume(self):
        return 4/3 * np.pi * self.r**3