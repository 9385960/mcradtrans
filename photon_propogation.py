from cloud import Cloud
import numpy as np

#TODO A simple framework. Many details still missing
class PhotonPath:
    #Initializes the photon object
    def __init__(self,direction,dl,cloud,scatteringFunc,emission_center,sphere):
        self.ta = 0
        self.d = direction
        self.c = cloud
        self.p = [0,0,0]
        self.error
        self.w
        #Computes the path through the cloud
        self.ComputePath()
        return
    #This function will compute the path through the cloud
    def ComputePath(self):
        #Executes while the photon is still inside the cloud
        while(self.GetDistFromCenter()-self.sphere.GetRadius() < 0):
            #Compute a new ts
            newTs = self.Get_ts()
            #Use the new ts to compute the distance to the next scattering event
            dist = self.GetUpdateDistance(newTs)
            #Update the current photon location
            self.UpdateLocation(self.d,dist)
            #Find a new direction
            self.UpdateDirection()
            #Increment the ta tot
            self.ta += (1/self.w-1)*newTs
        return
            
    #Computes the distance of the current photon position from the sphere center
    def GetDistFromCenter(self):
        d_to_r = self.p - self.sphere.GetCenter()
        return PhotonPath.GetMagnitude(d_to_r)
    #Updates the location based on a current direction and distance
    def UpdateLocation(self,direction,distance):
        self.p += direction *  distance
    #Computes a new photon trajectory
    def UpdateDirection(self):
        #Gets theta and phi from the scattering function
        (theta,phi) = scatteringFunc()
        #Turns data into unity vector in spherical coordinates
        dir_s = [1,theta,phi]
        #Returns the direction converted to rectangular
        return PhotonPath.SphericalToRectangular(dir_s)
    #Computes ts based on formula in paper
    def Get_ts(self):
        return -np.log(np.random.rand)
    #TODO still unclear how this works. paper says to increment tp until it is within error margine of ts
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
            #Increment tp based on approach in paper
            tp += self.GetSigma()*self.GetDensity()*self.dl
            #Increment the total distance
            dltot += self.dl
        return dltot
    #Computes W based on the formula in the paper
    def GetW(self):
        return np.exp(-self.ta)
    #Computes Sigma
    #TODO determine what sigma is and implment the function
    def GetSigma(self):
        return 1
    #TODO the paper says to muliply by nh we need to determine if this is really the cloud density
    def GetDensity(self):
        return self.c.GetDensity(self.p)
    
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
    