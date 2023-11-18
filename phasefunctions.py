
class PhaseFunctions:
    
    def HG_phase(self):
        r1 = np.random.rand()
        r2 = np.random.rand()
        numerator = (1+self.g**2)-((1-self.g**2)/(1-self.g+2*self.g*r1))**2
        denom = 2*self.g
        theta = numerator/denom
        phi = 2*np.pi*r2
        return(theta,phi)
    def Set_g(self,g):
        self.g = g
        return
    