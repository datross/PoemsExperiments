import numpy as np

prims = op('primitive1').prims
minWidth = op('const_size')['width']
minHeight = op('const_size')['height']
table = op('/project1/positions')


centers = []

class Center:
	def __init__(self, x, y):
		self.x = x
		self.y = y


def circular_order(centers):
    points = []
    newCoord = []

    for c in centers:
    	points.append((c.x, c.y))

    center = np.mean(points, axis=0)
    points = np.array(sorted(points, key=lambda x: np.angle((x-center)[0]+(x-center)[1]*1j)))
    
    for (x, y) in points:
        newCoord.append(Center(x, y))

    return newCoord

for p in prims:
	#print(p.size)
	if(p.size[0] > minWidth and p.size[1] > minHeight):
		centers.append(p.center)

table.setSize(len(centers), 2)

centers = circular_order(centers)

#file.write(line)
for i, c in enumerate(centers):	
	table[i, 0] = c.x
	table[i, 1] = c.y*2



		
op('createNodes').run()
