visualPath ='/project1/visuals'
shapeDetectionPath ='/project1/shapeDetection/geo1'

transforms = ops(visualPath+'/transformPos*')
points = ops(shapeDetectionPath+'/pointPos*')
copys = ops(shapeDetectionPath+'/copyPos*')

nbPeople = op('/project1/positions').numRows

def deleteNode(*names):
	for n in names:
		if op(n):
			op(n).outputConnectors[0].disconnect()
			op(n).inputConnectors[0].disconnect()
			op(n).destroy() 

def addTransform(name):
	if op(name):
		return

	trans = op(visualPath).create(transformTOP, name);
	op(trans).outputConnectors[0].connect(op(visualPath+'/compVisualPos'))
	op(trans).inputConnectors[0].connect(op(visualPath+'/visualPos'))
	op(trans).par.tx.expr = "op('/project1/positions')["+str(index+i)+", 0]"
	op(trans).par.ty.expr = "op('/project1/positions')["+str(index+i)+", 1]"
	if int(index+i)+1 == 0:
		op(trans).nodeY  = (op(trans).nodeHeight+10)*(index-i*2+1)
	else:
		op(trans).nodeY = (op(trans).nodeHeight+10)*(index+i)

def addPoints(namePoint, nameCopy):
	

	point = op(shapeDetectionPath).create(pointSOP, namePoint);
	copy = op(shapeDetectionPath).create(copySOP, nameCopy);

	op(copy).outputConnectors[0].connect(op(shapeDetectionPath+'/merge'))
	op(copy).inputConnectors[1].connect(op(shapeDetectionPath+'/circle'))
	op(copy).par.ncy = 1
	op(copy).nodeX  = (op(copy).nodeWidth+300)

	op(point).outputConnectors[0].connect(op(shapeDetectionPath+'/'+nameCopy))
	op(point).inputConnectors[0].connect(op(shapeDetectionPath+'/circle'))
	op(point).par.tx.expr = "op('/project1/pos"+str(index+i+1)+"')['tx']"
	op(point).par.ty.expr = "op('/project1/pos"+str(index+i+1)+"')['ty']"
	op(point).nodeX  = (op(copy).nodeWidth-100)

	if int(index+i)+1 == 0:
		y = (op(copy).nodeHeight+10)*(index-i*2+1)
	else:
		y = (op(copy).nodeHeight+10)*(index+i)

	op(copy).nodeY = y
	op(point).nodeY = -y


# on crée les transform pour les visuels
nbElem = min(len(points), len(transforms))
delta = nbElem - nbPeople;
index = nbElem

if delta > 0 : #on supprime des noeuds
	for i in range(1, delta+1):
		nameTrans = visualPath+'/transformPos'+str(int(index-i))
		namePoint = shapeDetectionPath+'/pointPos'+str(int(index-i))
		nameCopy = shapeDetectionPath+'/copyPos'+str(int(index-i))
		deleteNode(nameTrans, nameCopy, namePoint)
		
elif(delta < 0): #on ajout des noeuds
	for i in range(abs(delta)):
		nameTrans = 'transformPos'+str(int(index+i))
		namePoint = 'pointPos'+str(int(index+i))
		nameCopy = 'copyPos'+str(int(index+i))
		if not op(visualPath+'/'+nameTrans):
			addTransform(nameTrans)
		if not op(shapeDetectionPath+'/'+namePoint):
			addPoints(namePoint, nameCopy)
		





