import numpy as np
import pointgenerator

#A class for generating a cloud
class Cloud:
    #Initializes the cloud with side lengths L
    def __init__(self,L):
        self.l = L
        self.densityGrid = self._init_DensityGrid()
        self.points = self._init_Points()
    def _init_DensityGrid():
        densities = np.zeros((4,4,4))
        return densities
    def _init_Points():
        return 