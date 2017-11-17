import numpy as np
import cv2

from math import sin, cos, radians


# CALL -> (np_ndarray main_Image[,string name])
def saveImage(image, name='000'):
	cv2.imwrite('./Immagini/Acquisite/Imm_'+name+'.png', image)


# CALL -> (np_ndarray main_Image,array origin)
def getRotationMatrix(image,origin): 
	rot_center 	= (origin[0],origin[1])
	angle 		= origin[2]
	rot_mat 	= np.vstack([cv2.getRotationMatrix2D(rot_center, angle, 1.0), [0, 0, 1]])
	return rot_mat


# CALL -> (np_ndarray main_Image,array new_size[,array origin,string name])
def cropImage(image,new_imageSize,origin=[0,0,0],name='000'):
	#print origin 
	imageSize 	= tuple(new_imageSize)
	x_center 	= origin[0]
	y_center 	= origin[1]
	angle		= -origin[2]
	x_len 		= new_imageSize[0]
	y_len 		= new_imageSize[1]
	
	# # Taglio iniziale per diminuire i conti, DA SISTEMARE!!!
	# x0 		= int(x_center - x_len)
	# y0 		= int(y_center - y_len)
	# if x0<0 or y0<0:
	# 	return image[0:0,0:0]
	# image 	= image[y0:y0 + 2*y_len, x0:x0 + 2*x_len]
	# cv2.imwrite('ima.png',image)
	# # Applico rotazione
	# affine_mat 	= (np.matrix(getRotationMatrix(image,[x_len, y_len, angle])))[0:2, :]
	# rot_im 		= cv2.warpAffine(image, affine_mat , (2*x_len, 2*y_len), flags=cv2.INTER_LINEAR)

	# # Taglio finale
	# x1 		= int(x_len - x_len/2)
	# y1 		= int(y_len - y_len/2)
	# crop_im = rot_im[y1:y1 + y_len, x1:x1 + x_len]
	rot_mat = np.vstack([cv2.getRotationMatrix2D((x_center,y_center), angle, 1.0), [0, 0, 1]])
    
	affine_mat = (np.matrix(rot_mat))[0:2, :]
	rot_res = cv2.warpAffine(image, affine_mat , image.shape[:2], flags=cv2.INTER_LINEAR)

	x0 = int(origin[0]-x_len/2)
	y0 = int(origin[1]-y_len/2)
	crop_im = rot_res[y0:y0+y_len,x0:x0+x_len]


	saveImage(crop_im, name)
	return crop_im

# CALL -> (np_ndarray main_Image,array Samp_factors)
def downSample(image,factorOfSampling):
	new_xSize 	= image.shape[:2][0]/factorOfSampling[0]
	new_ySize 	= image.shape[:2][1]/factorOfSampling[1]
	new_im 		= cv2.pyrDown( image, dstsize=(new_xSize, new_ySize))
	return new_im


# CALL -> (np_ndarray main_Image,array Samp_factors)
def upSample(image,factorOfSampling):
	new_xSize 	= image.shape[:2][0]*factorOfSampling[0]
	new_ySize 	= image.shape[:2][1]*factorOfSampling[1]
	new_im 		= cv2.pyrUp( image, dstsize=(new_xSize, new_ySize))
	return new_im

# CALL -> imagePath, array regioni
# DA RIFARE CON OpenCV
def drawRegions(image,origins,Xdim,Ydim):


	for n in range(len(origins)):#range(0,len(self.origins)):
		alpha = radians(origins[n][2])
		ref_1 =[origins[n][0] - Xdim*cos(alpha) , origins[n][1] - Xdim*sin(alpha)] 
		ref_2 =[origins[n][0] + Xdim*cos(alpha) , origins[n][1] + Xdim*sin(alpha)]
		corner_1 =[ref_1[0] + Ydim*sin(alpha),ref_1[1] - Ydim*cos(alpha)]
		corner_2 =[ref_2[0] + Ydim*sin(alpha),ref_2[1] - Ydim*cos(alpha)]
		corner_3 =[ref_2[0] - Ydim*sin(alpha),ref_2[1] + Ydim*cos(alpha)]
		corner_4 =[ref_1[0] - Ydim*sin(alpha),ref_1[1] + Ydim*cos(alpha)]
		pts = np.array([corner_1,corner_2,corner_3,corner_4], np.int32)
		pts = pts.reshape((-1,1,2))
		cv2.polylines(image,[pts],True,(0,0,255),5)
		
	return image
	

def drawPath(image,curvePath):
	for i in range(1,len(curvePath)):
		cv2.line(image,(curvePath[i-1][0],curvePath[i-1][1]),(curvePath[i][0],curvePath[i][1]),(0,255,0),5)
	return image
	


 

################################################################################
##################################  NOTE  ######################################
################################################################################


# DA FARE DOWNSAMPLING TRA PIXEL MAIN E PIXEL IMMAGINI:
# se sottocampiono l'immagine di partenza ho problemi con l'origine
# se sottocampiono l'immagine ritagliata non ho buone performance
# se trovo la conversione pix_main pix_im non male, forse un po noioso da ridefinire gli array

