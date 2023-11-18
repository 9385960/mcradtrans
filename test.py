from cloud import Cloud
import matplotlib.pyplot as plt
from pointgenerator import PointGenerator
import numpy as np
import density_visualizer as dv

c = Cloud(2,10,1,2.3)

points = c.GetPoints()

#print(c.GetDensties())

#points = PointGenerator.UniformRejectionPointsInSphere(1000,1,np.array([0,0,0]))

#print(points)
#print(c.GetPoints())
x = points[:,0]
y = points[:,1]
z = points[:,2]

fig = plt.figure(figsize = (10, 10))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x, y, z, color = "green")
plt.title("simple 3D scatter plot")
 
# show plot
plt.show()

densities = c.GetDensties()
cube_length = c.GetSideLength()
divisions = c.GetDivisions()

biggest_density = np.max(densities)

sideLength = cube_length/divisions

cubes = [0]*divisions*divisions*divisions

index = 0

for i in range(divisions):
    for j in range(divisions):
        for k in range(divisions):
            bottom_left = [sideLength*i,sideLength*j,sideLength*k]
            normalized_den = densities[i][j][k]/biggest_density
            cubes[index] = dv.generate_cube(sideLength,bottom_left,[normalized_den,normalized_den,normalized_den,normalized_den])
            index += 1

dv.plot_cubes(cubes,additional_data=True,x=x,y=y,z=z)