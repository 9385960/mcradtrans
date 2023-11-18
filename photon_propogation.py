from cloud import Cloud
import numpy as np

class PhotonPath:
    def __init__(self,direction,dl,cloud,scatteringFunc,emission_center,sphere):
        self.ta = 0
        self.d = direction
        self.c = cloud
        self.p = [0,0,0]
        self.error
        self.w
        self.ComputePath()
        return
    
    def ComputePath(self):
        while(self.GetDistFromCenter()-self.sphere.GetRadius() < 0):
            newTs = self.Get_ts()
            dist = self.GetUpdateDistance(newTs)
            self.UpdateLocation(self.d,dist)
            self.UpdateDirection()
            self.ta += (1/self.w-1)*newTs
            
        
    def GetDistFromCenter(self):
        d_to_r = self.p - self.sphere.GetCenter()
        return PhotonPath.GetMagnitude(d_to_r)
    
    def UpdateLocation(self,direction,distance):
        self.p += direction *  distance
        
    def UpdateDirection(self):
        self.d = scatteringFunc()
        
    def Get_ts(self):
        return -np.log(np.random.rand)
    
    def GetUpdateDistance(self,ts):
        margine = self.error
        tp = 0
        dltot = 0
        while(np.abs(tp-ts)>margine):
            if(tp > ts):
                break
            tp += self.GetSigma()*self.GetDensity()*self.dl
            dltot += self.dl
        return dltot
    
    def GetW(self):
        return np.exp(-self.ta)
    
    @staticmethod
    def GetMagnitude(point):
        num = 0
        for i in range(len(point)):
            num += point[i]**2
        return np.sqrt(num)  
    