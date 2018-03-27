import numpy as np
from center import Center

prims = op('primitive1').prims

minWidth = op('min_size')['width']
minHeight = op('min_size')['height']

maxHeight = op('max_size')['height']
maxWidth = op('max_size')['width']

table = op('/project1/positions')


centers = []

def circular_order(centers):
	points = []
	newCoord = []

	for c,_ in centers:
		x = c.x
		y = c.y
		points.append((x, y))

	center = np.mean(points, axis=0)
	center = Center(center[0], center[1])
	# print(center)
	points = []
	
	for i, (c,f) in enumerate(centers):
		x = c.x
		y = c.y
		# nextId = (i+1)%len(centers)
		val = np.angle((x-center.x)+(y-center.y)*1j)
		points.append(((x, y), f, val))

	# points = np.array(sorted(points, key=lambda x: np.angle((x-center)[0]+(x-center)[1]*1j)))
	points.sort(key=lambda tup: tup[2])

	for c, f,_ in points:
		newCoord.append((Center(c[0], c[1]), f))

	return newCoord

for p in prims:
	#print(p.size)
	if(p.size[0] > minWidth and p.size[1] > minHeight):
		fat = (p.size[0] > maxWidth and p.size[1] > maxHeight)
		centers.append((p.center, fat))

table.setSize(len(centers), 3)
if len(centers)>0:
	centers = circular_order(centers)

#file.write(line)
for i, (c, f) in enumerate(centers):	
	table[i, 0] = c.x
	table[i, 1] = c.y*2
	table[i, 2] = f



		
# op('createNodes').run()
