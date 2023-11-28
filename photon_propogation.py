from cloud import Cloud
import numpy as np


class PhotonPath:
    #Initializes the photon object
    def __init__(self,direction,dl,cloud,scatteringFunc,sphere,initial_position,albedo,sigma,log_path = False,error_margine = 0.01,max_iters = 1000):
        self.ts_tot = 0
        self.sigma = sigma
        self.dl = dl
        self.ta = 0
        self.dist_traveled = 0
        self.d = direction
        self.c = cloud
        self.p = initial_position
        self.error = error_margine
        self.w = albedo
        self.sphere = sphere
        self.log_path = log_path
        self.scatteringFunc = scatteringFunc
        self.max_iters = max_iters
        if(log_path):
            self.path = []
        #Computes the path through the cloud
        self.ComputePath()
        return
    #This function will compute the path through the cloud
    def ComputePath(self):
        #Executes while the photon is still inside the cloud
        iters = 0
        while(self.GetDistFromCenter()-self.sphere.GetRadius() < 0 and iters < self.max_iters):
            #Compute a new ts
            newTs = self.Get_ts()
            #Use the new ts to compute the distance to the next scattering event
            (tp,dist) = self.GetUpdateDistance(newTs)
            #Update the current photon location
            self.UpdateLocation(self.d,dist)
            #Find a new direction
            self.d = self.UpdateDirection()
            #Increment the ta tot
            self.ta += (1/self.w-1)*tp
            iters += 1
        if(self.log_path):
            self.path.append(self.p.copy())
        return
            
    #Computes the distance of the current photon position from the sphere center
    def GetDistFromCenter(self):
        d_to_r = self.p - self.sphere.GetCenter().copy()
        return PhotonPath.GetMagnitude(d_to_r)
    #Computes the distance of the current photon position from the sphere center
    def GetPointFromCenter(self,point):
        d_to_r = point - self.sphere.GetCenter().copy()
        return PhotonPath.GetMagnitude(d_to_r)
    #Updates the location based on a current direction and distance
    def UpdateLocation(self,direction,distance):
        if(self.log_path):
            self.path.append(self.p.copy())
        self.p += direction *  distance
        return
    #Computes a new photon trajectory
    def UpdateDirection(self):
        #Gets theta and phi from the scattering function
        (theta,phi) = self.scatteringFunc()
        #Turns data into unity vector in spherical coordinates
        dir_s = [1,theta,phi]
        #Returns the direction converted to rectangular
        return PhotonPath.SphericalToRectangular(dir_s)
    #Computes ts based on formula in paper
    def Get_ts(self):
        return -np.log(np.random.rand())
    #Increments the path based on some new tprime
    def GetUpdateDistance(self,ts):
        #The error margine
        margine = self.error
        #Initializes tp and dltot
        tp = 0
        dltot = 0
        #While the difference is outside the error margine increment tp
        while(np.abs(tp-ts)>margine):
            #Needed to avoid infinite loop if tp is bigger than ts and outside error margine
            #We only increase, so the error will just get larger and larger and won't approach ts
            if(tp > ts):
                break
            new_point = self.p + dltot*self.d
            if(self.GetPointFromCenter(new_point) > self.sphere.GetRadius()):
                break
            #Increment tp based on approach in paper
            tp += self.GetSigma()*self.GetDensity(new_point)*self.dl
            #Increment the total distance
            dltot += self.dl
        self.dist_traveled += dltot
        self.ts_tot += tp
        return (tp,dltot)
    
    def GetPath(self):
        return self.path
    #Computes W based on the formula in the paper
    def GetW(self):
        return np.exp(-self.ta)
    #Returns Tau_a
    def GetTa(self):
        return self.ta
    #Returns the total distance traveled
    def GetDistTot(self):
        return self.dist_traveled
    #Returna Sigma
    def GetSigma(self):
        return self.sigma
    #Gets the density at the point specified
    def GetDensity(self,point):
        return self.c.GetDensityInterpolated(point)
    #Returns the total ts experienced by the photon
    def GetTsTot(self):
        return self.ts_tot
    def GetEndPos(self):
        return self.p
    #Method to get the magnitude of a vector
    @staticmethod
    def GetMagnitude(point):
        num = 0
        for i in range(len(point)):
            num += point[i]**2
        return np.sqrt(num)  
    #Function to convert spherical to rectangular
    @staticmethod
    def SphericalToRectangular(p):
        r = p[0]
        t = p[1]
        phi = p[2]
        x = r*np.sin(t)*np.cos(phi)
        y = r*np.sin(t)*np.sin(phi)
        z = r*np.cos(t)
        return np.array([x,y,z])
    