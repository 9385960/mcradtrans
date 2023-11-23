import numpy as np

class Sphere:
    
    def __init__(self,r,c):
        self.r = r
        self.c = c
        return
    def GetRadius(self):
        return self.r
    def GetCenter(self):
        return self.c
    def GetVolume(self):
        return 4/3 * np.pi * self.r**3