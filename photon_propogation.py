from cloud import Cloud

class PhotonPath:
    def __init__(self,direction,dl,cloud,scatteringFunc):
        self.ta = 0
        self.d = direction
        self.c = cloud
        self.p = [0,0,0]
        return
    
    def UpdateLocation(self,direction,distance):
        self.p += direction *  distance
    def UpdateDirection(self):
        self.d = scatteringFunc()
             
    