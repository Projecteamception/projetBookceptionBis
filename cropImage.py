from PIL import Image
from pprint import pprint

seuil = 150
third = 1/3


def cropImage(imgName):
	global image1
	image1 = Image.open(imgName)
	global pix 
	pix = image1.load()
	global width, height 
	width, height = image1.size

	#Transformer en bicolor
	for i in range(height):
		for j in range(width):

			r, g, b = image1.getpixel((j, i))
			brightness = third * r + third * g + third * b

			if brightness > seuil:
				#white pix
				pix[j,i] = (255,255,255)
			else:
				#black pix
				pix[j,i] = (0,0,0)


def showCropped():
	#From Top
	box = (getFirstBlack(3,image1), getFirstBlack(1,image1), getFirstBlack(4,image1), getFirstBlack(2,image1))
	area = image1.crop(box)
	area.show()
	print("Image cropped")

def getFirstBlack(fromW, img):
	#fromW -> 1(top) 2(bottom) 3(left) 4(right)
	cacheLimit = 0
	storedValue = False

	if fromW == 1:
		for i in range(height):
			for j in range(width):

				r, g, b = img.getpixel((j, i))
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	elif fromW == 2:
		for i in range(height-1,0,-1):
			for j in range(width):

				r, g, b = img.getpixel((j, i))
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	elif fromW == 3:
		for i in range(width):
			for j in range(height):

				r, g, b = img.getpixel((i, j))
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True
				
	elif fromW == 4:
		for i in range(width-1,0,-1):
			for j in range(height):

				r, g, b = img.getpixel((i, j))
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	return cacheLimit





