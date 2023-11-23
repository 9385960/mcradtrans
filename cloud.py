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
    #num_divisions, how many divisions each axis should be broken up into to generate subcubes
    def __init__(self,L,num,power,D,num_divisions = 4, particle_mass = 1,density_offset = 0,seed = 0):
        #Initializes the paramters
        self.n = num
        self.d = D
        self.pow = power-1
        self.l = L
        self.divisions = num_divisions
        self.m = particle_mass
        self.doffset = density_offset
        #Sets random number generator seed
        PointGenerator.SetSeed(seed)
        #Gets the points inside the cube
        self.points = self._init_Points()
        #Determines the density grid
        self.densityGrid = self._init_DensityGrid()
    #Computes a density grid
    def _init_DensityGrid(self):
        #Currently a density grid of all zeros returned
        densities = np.zeros((self.divisions,self.divisions,self.divisions))
        length = self.l/self.divisions
        for i in range(len(self.points)):
            point = self.points[i]
            x_index = (int)(np.floor(point[0]/length))
            y_index = (int)(np.floor(point[1]/length))
            z_index = (int)(np.floor(point[2]/length))
            densities[x_index,y_index,z_index] += self.m
        
        volume = (length)**(3)
        
        for i in range(len(densities)):
            for j in range(len(densities[i])):
                for k in range(len(densities[i][j])):
                    densities[i][j][k] = densities[i][j][k]/volume + self.doffset
            
        return densities
    def _init_Points(self):
        #Initalizes the prev points to random points in the cube
        prevPoints = PointGenerator.GeneratePointsInBox(self.n,self.l)
        #Will make N* len(prevPoints) new points in the array
        for i in range(self.pow):
            #Makes a new array of lerger length
            newPoints = np.zeros((len(prevPoints)*self.n,3))
            #Gets N new points for each point to determine the 
            for i in range(len(prevPoints)):
                delta = np.exp(np.log(self.n)/self.d)
                radius = self.l/(2*delta)
                newPoints[i*self.n:(i+1)*self.n] = PointGenerator.UniformRejectionPointsInSphere(self.n,radius,prevPoints[i])
            prevPoints = newPoints
        
        self._wrap_Points(prevPoints)
        return prevPoints
    #Needs to check that all points lie inside the cube and if any fall outside the cube they should be wrapped around to the other side
    def _wrap_Points(self,points):
        #Loops over all points
        for i in range(len(points)):
            #Checks if x is outside [0,L] and updates it accordingly
            if(points[i][0] < 0):
                while(points[i][0] < 0):
                    points[i][0] += self.l
            elif(points[i][0] > self.l):
                while(points[i][0] > self.l):
                    points[i][0] -= self.l
            #Checks if y is outside [0,L] and updates it accordingly
            if(points[i][1] < 0):
                while(points[i][1] < 0):
                    points[i][1] += self.l
            elif(points[i][1] > self.l):
                while(points[i][1] > self.l):
                    points[i][1] -= self.l
            #Checks if z is outside [0,L] and updates it accordingly
            if(points[i][2] < 0):
                while(points[i][2] < 0):
                    points[i][2] += self.l
            elif(points[i][2] > self.l):
                while(points[i][2] > self.l):
                    points[i][2] -= self.l
        return points
    #Method to get points
    def GetPoints(self):
        return self.points
    #Method to get densities
    def GetDensties(self):
        return self.densityGrid
    #Method to get the number of divisions
    def GetDivisions(self):
        return self.divisions
    #Method to return side length
    def GetSideLength(self):
        return self.l
    #Method to get densities
    #TODO Need to implement interpolation
    def GetDensity(self,point):
        length = self.l/self.divisions
        #Checks if the point is inside the cube
        if(point[0]<0 or point[1]<0 or point[2]<0):
            return 0
        if(point[0]>self.l or point[1]>self.l or point[2]>self.l):
            return 0
        #Gets the density in the cube that the point lies in if it is inside the total domain
        x_index = (int)(np.floor(point[0]/length))
        y_index = (int)(np.floor(point[1]/length))
        z_index = (int)(np.floor(point[2]/length))
        
        return self.densityGrid[x_index,y_index,z_index]