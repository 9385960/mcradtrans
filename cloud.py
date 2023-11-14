import numpy as np
from pointgenerator import PointGenerator

#A class for generating a cloud
class Cloud:
    #Initializes the cloud
    #Input parameters are:
    #L, the side lengths of the cube
    #num, the number of points to be generated raised to some power
    #power, the power that will raise the number of points by so that Ntot = num^power
    #D, the fractal dimension of the cloud
    def __init__(self,L,num,power,D):
        #Initializes the paramters
        self.n = num
        self.d = D
        self.pow = power
        self.l = L
        #Determines the density grid
        self.densityGrid = self._init_DensityGrid()
        #Gets the points inside the cube
        self.points = self._init_Points()
    #Computes a density grid
    def _init_DensityGrid(self):
        #TODO implement the density grid as described in the paper
        #Currently a density grid of all zeros returned
        densities = np.zeros((4,4,4))
        return densities
    def _init_Points(self):
        #Initalizes the prev points to random points in the cube
        prevPoints = PointGenerator.GeneratePointsInBox(self.n,self.l)
        #Will make N* len(prevPoints) new points in the array
        for i in range(self.pow):
            #Makes a new array of lerger length
            newPoints = np.zeros((len(prevPoints)*self.n),3)
            #Gets N new points for each point to determine the 
            for i in range(len(prevPoints)):
                delta = np.exp(np.log(self.n)/self.d)
                radius = self.l/(2*delta)
                newPoints[i*self.n:(i+1)*self.n] = PointGenerator.GeneratePointsInSphere(self.n,radius,prevPoints[i])
            prevPoints = newPoints
        return prevPoints
    #Needs to check that all points lie inside the cube and if any fall outside the cube they should be wrapped around to the other side
    def _wrap_Points(self,points):
        #TODO implment point wrapping
        return points