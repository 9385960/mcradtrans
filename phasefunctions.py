import numpy as np

#Class which will contain phase functions
class PhaseFunctions:    
    #intializes the object
    def __init__(self):
        self.currentPhaseFunc = 0
        self.g = 0.2   
    #The HG phase function as defined in the paper
    def HG_phase(self):
        r1 = np.random.rand()
        r2 = np.random.rand()
        numerator = (1+self.g**2)-((1-self.g**2)/(1-self.g+2*self.g*r1))**2
        denom = 2*self.g
        theta = numerator/denom
        phi = 2*np.pi*r2
        return(theta,phi)
    #Allows g to be set
    def Set_g(self,g):
        self.g = g
        return
    #Gets the scatter direction. It allows for multiple phase functions to be used
    def GetScatterDirection(self):
        if(self.currentPhaseFunc == 0):
            return self.HG_phase()
        else:
            return 0
    