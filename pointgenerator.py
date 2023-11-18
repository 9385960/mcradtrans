import numpy as np

#Class for generating random points
class PointGenerator:
    #Allows for a seed to be set for pseudo random number generation
    @staticmethod
    def SetSeed(seed):
        np.random.seed(seed)
        return
    #Generates N points uniformly inside a box
    @staticmethod
    def GeneratePointsInBox(N,L):
        points = L*np.random.rand(N,3)
        return points
    #Generates points uniformly inside a sphere
    @staticmethod
    def UniformPointsInSphere(N,R,C):
        points = np.random.rand(N,3)
        for i in range(N):
            point = points[i]
            point[0] = (point[0]**(1/3))* R
            point[1] = np.arccos(2*point[1]-1)
            point[2] = point[2] * 2 * np.pi
            point = PointGenerator.SphericalToRectangular(point)
            point += C
            points[i] = point
        
        return points
    #Generates points uniformly inside a sphere by sampling in a rectangle and rejecting those points that lie outside the sphere
    @staticmethod
    def UniformRejectionPointsInSphere(N,R,C):
        points = np.random.rand(N,3)
        for i in range(N):
            point = points[i]
            pointAccepted = False
            while(not pointAccepted):
                point[0] = 2*R*point[0]-R
                point[1] = 2*R*point[1]-R
                point[2] = 2*R*point[2]-R
                if(np.sqrt(point[0]**2+point[1]**2+point[2]**2)>R):
                    point = np.random.rand(3)
                else:
                    pointAccepted = True
            point += C
            points[i] = point
        
        return points
    #Non uniform generation of points in a sphere
    #Should be avoided
    @staticmethod
    def GeneratePointsInSphere(N,R,C):
        points = np.random.rand(N,3)
        for i in range(N):
            point = points[i]
            point[0] = point[0] * R
            point[1] = point[1] * np.pi
            point[2] = point[2] * 2 * np.pi
            point = PointGenerator.SphericalToRectangular(point)
            point += C
            points[i] = point
        
        return points
    #Generates points on the surface of a sphere
    #Most likely not uniformly generated
    #Theta is not picked properly
    @staticmethod
    def GeneratePointsOnSphere(N,R,C):
        points = np.random.rand(N,3)
        for i in range(N):
            point = points[i]
            point[0] = R
            point[1] = point[1] * np.pi
            point[2] = point[2] * 2 * np.pi
            point = PointGenerator.SphericalToRectangular(point)
            point += C
            points[i] = point
        
        return points
    #Converts spherical to rectangular coordinates
    @staticmethod
    def SphericalToRectangular(p):
        r = p[0]
        t = p[1]
        phi = p[2]
        x = r*np.sin(t)*np.cos(phi)
        y = r*np.sin(t)*np.sin(phi)
        z = r*np.cos(t)
        return np.array([x,y,z])