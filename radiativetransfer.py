import numpy as np

def weight(tau_a_tot):
    return np.exp(-tau_a_tot)

def tau_s(p):
    return -np.log(p)

def phi(theta,g):
    num = (1/(4*np.pi))(1-g**2)
    denom = (1+g**2-2*g*np.cos(theta))**(3/2)
    return num/denom

def theta(p,g):
    num = (1+g**2)-np.abs((1-g**2)/(1-g+2*g*p))**2
    denom = 2*g
    return num/denom

def azimuthal(p):
    """Defined after eqn (A5), gives the azimuthal angle as a function of a random variable p (different p from theta)"""
    return 2*np.pi*p
    
