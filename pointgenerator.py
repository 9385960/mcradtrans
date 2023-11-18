import numpy as np

class PointGenerator:
    @staticmethod
    def GeneratePointsInBox(N,L):
        points = L*np.random.rand(N,3)
        return points
        
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
    
    @staticmethod
    def SphericalToRectangular(p):
        r = p[0]
        t = p[1]
        phi = p[2]
        x = r*np.sin(t)*np.cos(phi)
        y = r*np.sin(t)*np.sin(phi)
        z = r*np.cos(t)
        return np.array([x,y,z])