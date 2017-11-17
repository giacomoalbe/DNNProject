import myLibrary

from myLibrary import Camera, DataSet, cv


data 		= DataSet("./curvePath/CircleData.txt")
curvePath	= data.getInput()
# # solo perche simulo ingressi
# curvePath[2] = [i%360 for i in curvePath[2]]
# for i in range(len(curvePath[2])):
#     if 0<=curvePath[2][i]<=90:
#         pass
#     elif 90<curvePath[2][i]<=180:
#         curvePath[2][i]=(curvePath[2][i]-90)
#     elif 180<curvePath[2][i]<=270:
#         curvePath[2][i]=-(curvePath[2][i]-180)
#     else:
#         curvePath[2][i]=-(curvePath[2][i]-180-90)

print 'Lunghezza curva: ', len(curvePath)
print

cam = Camera()

cam.get_AcqPoints(curvePath)
imagesNumber = cam.get_AcqImages()
print "Numero immagini: ", imagesNumber
print 'Punti di origine'
for i in range(len(cam.origins)):
	print cam.origins[i]
print

mainWithRegions = cam.get_Path(curvePath)
mainWithPath 	= cam.get_Regions()
mainWithBoth    = cam.get_Draw(curvePath)

