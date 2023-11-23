from cloud import Cloud
import matplotlib.pyplot as plt
from pointgenerator import PointGenerator
import density_visualizer as d_v
c = Cloud(2,10,3,2.3,num_divisions=4,density_offset=1)

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

cubes = d_v.generate_cubes(densities,cube_length,divisions)

d_v.plot_cubes(cubes,additional_data=True,x=x,y=y,z=z)