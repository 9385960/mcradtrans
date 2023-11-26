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
    #Method to get densities without interpolation
    def GetDensity(self,point):
        length = self.l/self.divisions
        #Checks if the point is inside the cube
        if(point[0]<0 or point[1]<0 or point[2]<0):
            return 0
        if(point[0]>=self.l or point[1]>=self.l or point[2]>=self.l):
            return 0
        #Gets the density in the cube that the point lies in if it is inside the total domain
        x_index = (int)(np.floor(point[0]/length))
        y_index = (int)(np.floor(point[1]/length))
        z_index = (int)(np.floor(point[2]/length))
        
        return self.densityGrid[x_index,y_index,z_index]
    def GetDensityInterpolated(self,point):
        (vals,index) = self.__get_interpolation__vals(point)
        bottom_left = self.__get_density_position(index[0][0],index[0][1],index[0][2])
        top_right = self.__get_density_position(index[7][0],index[7][1],index[7][2])

        xd = (point[0] - bottom_left[0])/(top_right[0] - bottom_left[0])
        yd = (point[1] - bottom_left[1])/(top_right[1] - bottom_left[1])
        zd = (point[2] - bottom_left[2])/(top_right[2] - bottom_left[2])

        return self.__trilinear_interpolation__(xd,yd,zd,vals)
    def __trilinear_interpolation__(self,xd,yd,zd,vals):
        c00 = vals[0]*(1-xd) + vals[4]*xd
        c01 = vals[1]*(1-xd) + vals[5]*xd
        c10 = vals[2]*(1-xd) + vals[6]*xd
        c11 = vals[3]*(1-xd) + vals[7]*xd

        c0 = c00*(1-yd)+c10*yd
        c1 = c01*(1-yd)+c11*yd
        return c0*(1-zd) + c1*zd
    def __get_density_position(self,x_index,y_index,z_index):
        length = self.l/self.divisions
        x = x_index*length + length/2
        y = y_index*length + length/2
        z = z_index*length + length/2
        return np.array([x,y,z])
    def __get_interpolation__vals(self,point):
        length = self.l/self.divisions
        translated_point = point - length/2
        #Gets the density in the cube that the point lies in if it is inside the total domain
        x_i = (int)(np.floor(translated_point[0]/length))
        y_i = (int)(np.floor(translated_point[1]/length))
        z_i = (int)(np.floor(translated_point[2]/length))
        c000i = [x_i,y_i,z_i]
        c100i = [x_i+1,y_i,z_i]
        c010i = [x_i,y_i+1,z_i]
        c110i = [x_i+1,y_i+1,z_i]
        c001i = [x_i,y_i,z_i+1]
        c101i = [x_i+1,y_i,z_i+1]
        c011i = [x_i,y_i+1,z_i+1]
        c111i = [x_i+1,y_i+1,z_i+1]
        indices = np.array([c000i,c001i,c010i,c011i,c100i,c101i,c110i,c111i],dtype=int)
        vals = np.zeros(8)
        for i in range(len(indices)):
            outside_bounds = False
            for j in range(len(indices[i])):
                if(indices[i][j] < 0 or indices[i][j] >= (int)(self.divisions)):
                    outside_bounds = True
            if(outside_bounds):
                vals[i] = 0
            else:
                vals[i] = self.densityGrid[indices[i][0],indices[i][1],indices[i][2]]

        return (vals,indices)
    
    def GetNumPointsInsideSphere(self,s):
        sphere_center = s.GetCenter()
        points = self.points

        num_points_in_sphere = 0

        for i in range(len(points)):
            vec = points[i]-sphere_center
            distance = Cloud.GetMagnitude(vec)
            if(distance <= s.GetRadius()):
                num_points_in_sphere += 1

        return num_points_in_sphere
    
    #Method to get the magnitude of a vector
    @staticmethod
    def GetMagnitude(point):
        num = 0
        for i in range(len(point)):
            num += point[i]**2
        return np.sqrt(num)