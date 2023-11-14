from cloud import Cloud
import matplotlib.pyplot as plt

c = Cloud(1,10,3,10)

print(len(c.GetPoints()))
#print(c.GetPoints())
x = c.GetPoints()[:,0]
y = c.GetPoints()[:,1]
z = c.GetPoints()[:,2]

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x, y, z, color = "green")
plt.title("simple 3D scatter plot")
 
# show plot
plt.show()