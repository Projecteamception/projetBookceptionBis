from PIL import Image
from pprint import pprint

seuil = 150
ystart, yend = 0, 0
xstart, xend = 0, 0
result = []

imageName = str(input("Name of image:"))

image1 = Image.open(imageName)
pix = image1.load()
width, height = image1.size


def getFirstBlack(fromW, img):
	#fromW -> 1(top) 2(bottom) 3(left) 4(right)
	cacheLimit = 0
	storedValue = False

	if fromW == 1:
		for i in range(height):
			for j in range(width):

				r, g, b = img.getpixel((j, i))
				pix = img.load()
				third = 1/3
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	if fromW == 2:
		for i in range(height-1,0,-1):
			for j in range(width):

				r, g, b = img.getpixel((j, i))
				pix = img.load()
				third = 1/3
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	if fromW == 3:
		for i in range(width):
			for j in range(height):

				r, g, b = img.getpixel((i, j))
				pix = img.load()
				third = 1/3
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True
				
	if fromW == 4:
		for i in range(width-1,0,-1):
			for j in range(height):

				r, g, b = img.getpixel((i, j))
				pix = img.load()
				third = 1/3
				brightness = third * r + third * g + third * b

				if brightness < seuil:
					#black pix
					if not storedValue:
						cacheLimit = i
						storedValue = True

	return cacheLimit

#Transformer en bicolor
for i in range(height):
	for j in range(width):

		r, g, b = image1.getpixel((j, i))
		pix = image1.load()
		third = 1/3
		brightness = third * r + third * g + third * b

		if brightness > seuil:
			#white pix
			pix[j,i] = (255,255,255)
		else:
			#black pix
			pix[j,i] = (0,0,0)

#From Top
ystart = getFirstBlack(1,image1)
print(ystart)
box = (getFirstBlack(3,image1), getFirstBlack(1,image1), getFirstBlack(4,image1), getFirstBlack(2,image1))
area = image1.crop(box)
area.show()
a = input()

