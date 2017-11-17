import myOpencv as cv 

from math import sin, cos, asin, acos, fabs, radians


class Camera:

	
	def __init__(self,  modelPath = "./ModelliCamera/Modello_03.txt"):
		self.modelPath = modelPath
		
		# CARICO MODELLO CAMERA
		try:
			self.model = open(modelPath,'r')
			stampaModel = open(modelPath,'r')
			
		except OSError as e:
			print('LoadError: File non caricato', e)
			# selezionare file
			exit()
		for line in stampaModel:
			line = line.strip('\r\n')
			print line

		for l in self.model:
			string = l.split(':')
			#for n in range(len(string)):
			#	string[n] = string[n].strip('\t\t\t\t')
			string[-1] = string[-1].strip('\r\n')
			
			if string[0] 	== "sensorSize":
				self.sensorSize 	= [int(string[1]),int(string[2])]
				#print self.sensorSize
				continue 
			elif string[0] 	== "Resolution":
				self.Resolution 	= [int(string[1]),int(string[2])]
				#print self.Resolution
				continue
			elif string[0] 	== "focalLength":
				self.focalLength 	= int(string[1])
				#print self.focalLength
				continue
			elif string[0] 	== "ShutterSpeed":
				self.ShutterSpeed 	= int(string[1])
				#print self.ShutterSpeed
				continue
			elif string[0] 	== "DiametroLente":
				self.DiametroLente 	= int(string[1])
				#print self.DiametroLente
				continue
			elif string[0] 	== "f-number":
				self.f_number		= int(string[1])
				#print self.f_number
				continue
			elif string[0] 	== "ISO":
				self.ISO			= int(string[1])
				#print self.ISO
				continue
			elif string[0] 	== "MaxDisplacementX":
				self.MaxDispX		= int(string[1])
				#print self.MaxDispX
				continue
			elif string[0] 	== "MaxDisplacementY":
				self.MaxDispY		= int(string[1])
				#print self.MaxDispY
				continue
			elif string[0] 	== "CofC(b)":
				self.b 				= int(string[1])
				#print self.b
				continue
			elif string[0] 	== "ErrTollerance":
				self.Err_Z			= int(string[1])
				#print self.Err_Z
				continue
			elif string[0] 	== "Sampling Time":
				self.T_s			= int(string[1])
				#print self.T_s
				continue
			elif string[0] 	== "HdaTerra(Z)":
				self.Z = int(string[1])
				#print self.Z
				continue

		# Definisco Attributi Indiretti, da fare in formato quantizzato rispetto Main	
		try:
			print 'PARAMETRI OTTENUTI'
			# Dimensione pixel in mm
			self.pixDim 	= [self.Z*self.sensorSize[0]/self.Resolution[0]/self.focalLength,
						self.Z*self.sensorSize[1]/self.Resolution[1]/self.focalLength]
			# Dimensione Immagine in mm
			self.imageDim 	= [self.Z*self.sensorSize[0]/self.focalLength,
						self.Z*self.sensorSize[1]/self.focalLength]
			
			self.aperture	= self.DiametroLente/self.f_number
			
			temp1 			= (self.Z + self.focalLength)*(self.aperture+self.b)/(self.aperture+self.b*(self.Z + self.focalLength)/self.focalLength) 
			temp2 			= (self.Z + self.focalLength)*(self.aperture-self.b)/(self.aperture-self.b*(self.Z + self.focalLength)/self.focalLength)
			self.DoF		= fabs(temp1-temp2)
			print 'Dimensione Pixel [mm] 		:',self.pixDim	
			print 'Dimensione Immagine [mm] 	:',self.imageDim
			print 'Diametro Effettivo Lente [mm]	:',self.aperture
		except AttributeError as e:
			print 'LoadError: Errore in parsing',e
			exit()

		print
		# CAMERA PATH
		self.origins = []

	def get_AcqPoints(self,curvePath):
		try:
			T = self.T_s
			print 'Tempo di campionamento da Modello: ',T
			val = raw_input('Mantenere invariato il Tempo di campionamento(y/n)? ')
			print val
		except AttributeError as e:
			print 'Tempo di campionamento non caricato correttamente'		
			val = 'n'
		if val=='y':
			Tc = self.T_s
		else:
			Tc = int(input('Inserire Tempo di campionamento desiderato: '))

		pointNumber = int(len(curvePath)/Tc)+1
		origins = []
		print
		print 'Numero punti percorso: ' ,len(curvePath)
		print 'Numero punti origine: ' ,pointNumber 
		print
		for i in range(0,(len(curvePath)),Tc): #verificare
			try:
				origins.append(curvePath[i])
			except IndexError:
				print 'getOriginError: Errore ad iterazione', i
			
		self.origins = origins
		return origins	

	def get_AcqImages(self,imagePath = "./Immagini/Main_01.png"):
		main = cv.cv2.imread(imagePath)
		for i in range(len(self.origins)):
			cv.cropImage(main, self.imageDim, self.origins[i],str(i))# CALL -> (np_ndarray main_Image,array new_size[,array origin,string name])
		return i+1# Numero immagini Prodotte 


	# DA RIFARE CON openCV
	def get_Regions(self,imagePath = "./Immagini/Main_01.png"):
		image = cv.cv2.imread(imagePath)
		if len(self.origins)==0:
			print('Acquisition Points not defined')
			end()
		Xdim = int(self.imageDim[0]/2)
		Ydim = int(self.imageDim[1]/2)
		print "Dimensione Regioni " ,Xdim*2, Ydim*2
		image = cv.drawRegions(image,self.origins,Xdim,Ydim)
		cv.cv2.imwrite("./Immagini/ImageWithRegions.png",image)
		return  image
		

	def get_Path(self,curvePath,imagePath = "./Immagini/Main_01.png"):
		image = cv.cv2.imread(imagePath)
		image = cv.drawPath(image,curvePath)
		cv.cv2.imwrite("./Immagini/ImageWithPath.png",image)
		return image

	def get_Draw(self,curvePath,imagePath = "./Immagini/Main_01.png"):
		if len(self.origins)==0:
			print('Acquisition Points not defined')
			end()
		Xdim = int(self.imageDim[0]/2)
		Ydim = int(self.imageDim[1]/2)
		print "Dimensione Regioni " ,Xdim*2, Ydim*2
		image = cv.cv2.imread(imagePath)
		image = cv.drawPath(image,curvePath)
		image = cv.drawRegions(image,self.origins,Xdim,Ydim)
		cv.cv2.imwrite("./Immagini/ImageWithDraw.png",image)
		return image

class DataSet:
	def __init__(self,filePath):
		try:
			self.file = open(filePath,'r')
			
		except FileNotFoundError:
			print('LoadError: File non caricato')
			exit()

	def getInput(self): #ho anche angolo traiettoria
		X 			= []
		Y 			= []
		Theta 		= []
		curvePath 	= []

		for l in self.file:
			line 	= l.split('\t',2)
			line[-1]= line[-1].strip()
			#print(line,len(line))
			for i in range(3):
				pass
				#print(i)
				if line[i] == 'X':
			 		Xcol 	= i
			 		#print('Xcol is ',Xcol) 
				if line[i] == 'Y':
			 		Ycol 	= i
			 		#print('Ycol is ',Ycol)
				if line[i] == 'Theta':
			 		Thetacol= i
			 		#print('Thetacol is ',Thetacol)
			try:
		 		X.append(float(line[Xcol]))
		 		
			except NameError:
		 		pass
			except ValueError:
		 		pass
			try:
		 		Y.append(float(line[Ycol]))
		 		#print('values ', X,Y)
			except NameError:
		 		pass
			except ValueError:
		 		pass
			try:
		 		Theta.append(float(line[Thetacol]))
		 		#print('values ', X,Y)
			except NameError:
		 		pass
			except ValueError:
		 		pass
		
		try:
			if len(X)!=len(Y) or len(Y)!=len(Theta) or len(X)!=len(Theta):
				print 'LoadError: DataSet danneggiato, Lunghezze input diverse'
			length = [len(X),len(Y),len(Theta)]
			data_len = min(length)
			if data_len == 0:
				print 'LoadError: DataSet danneggiato'
				exit()
			# Save in array con conversione [mm]->[pixMain]
			pix_size = [1,1]
			for i in range(data_len):
				X[i] = int(X[i]/pix_size[0])
				Y[i] = int(Y[i]/pix_size[1])				
				curvePath.append([X[i],Y[i],Theta[i]])  
		except NameError as e:
			print 'LoadError: DataSet non letto correttamente' ,e
			exit()
		
		


		return curvePath

	def getOutput(self):
		# leggo da stesso file colonne diverse per velocita e Yaw_rate
		pass

		