from cloud import Cloud
import matplotlib.pyplot as plt
from pointgenerator import PointGenerator
import numpy as np


#c = Cloud(1,10,3,10)

#points = c.GetPoints()

points = PointGenerator.UniformPointsInSphere(10000,1,np.array([0,0,0]))

#print(points)
#print(c.GetPoints())
x = points[:,0]
y = points[:,1]
z = points[:,2]

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x, y, z, color = "green")
plt.title("simple 3D scatter plot")
 
# show plot
plt.show()