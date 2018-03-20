from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from tkinter import *
from PIL import Image, ImageTk, Image, ImageDraw, ImageFont
import math
import sys
import os

print("STARTING LINEASOFT V2.0.4....")
#id des cams
camId1 = 0
camId2 = 1
camId3 = 2

cam1isValid = False
cam2isValid = False
cam3isValid = False

#définir les camId en fonction des params du fichier

with open("cam_param", "r") as ins:
    for num in ins:

        if num.split("=")[0] == "c1":
            camId1 = int(num.split("=")[1])
        elif num.split("=")[0] == "c2":
            camId2 = int(num.split("=")[1])
        elif num.split("=")[0] == "c3":
            camId3 = int(num.split("=")[1])
        elif num == "END":
            break


#des des positions et cams
xpos = 100#position du robot définie par le logiciel
ypos = 100
xposexp = 100#position du robot définie par les caméras
yposexp = 100

camangle1 = float(0)
camangle2 = float(0)
camangle3 = float(0)

camDroite = [[0,0],[0,0],[0,0]]
camDroite[0][0] = 0#coefficient directeur de la caméra 0

camposX = [0,0,0]
camposY = [0,0,0]

camposX[0] = 0
camposX[1] = 0
camposY[0] = 0
camposY[1] = 0

bisseX1 = 0

camopenangle = 40

currentVector = "2x+4"
#-------------------

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
redLower = (105, 100, 100)
redUpper = (300, 255, 255)

redLower2 = (0, 70, 50)
redUpper2 = (30, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas

#------------------------------

master = Tk()
master.geometry("1300x800")
      
master.grid()
master.title("Grid Manager")

for r in range(6):
    master.rowconfigure(r, weight=1)    
for c in range(5):
    master.columnconfigure(c, weight=1)
#Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

#get list of cams and all the related stuff


cams = LabelFrame(master, text="cameras")
cams.grid(row = 0, column = 0, rowspan = 2, columnspan = 1, sticky = W+E+N+S) 

cam1 = Frame(cams)
cam1.pack()
cam2 = Frame(cams)
cam2.pack()
cam3 = Frame(cams)
cam3.pack()

#open the cameras depending on the index
try:
    captest = cv2.VideoCapture(camId1)
    _, frame1 = captest.read()
    cv2.imshow('frame',frame1)
    captest.release()
    cv2.destroyAllWindows()
    cam1isValid = True
    print("cam 1 is properly plugged")
except:
    cam1isValid = False
    print("cam 1 is not properly plugged")


try:
    cap2test = cv2.VideoCapture(camId2)
    _, frame2 = cap2test.read()
    cv2.imshow('frame',frame2)
    cap2test.release()
    cv2.destroyAllWindows()
    cam2isValid = True
    print("cam 2 is properly plugged")
except:
    cam2isValid = False
    print("cam 2 is not properly plugged")



try:
    cap3test = cv2.VideoCapture(camId3)
    _, frame3 = cap3test.read()
    cv2.imshow('frame',frame3)
    cap3test.release()
    cv2.destroyAllWindows()
    cam3isValid = True
    print("cam 3 is properly plugged")
except:
    cam3isValid = False
    print("cam 3 is not properly plugged")
    

image = Image.open("unplugged.png")
image = image.resize((160, 120), Image.ANTIALIAS) #The (250, 250) is (height, width)
imageup = ImageTk.PhotoImage(image)

#reopend authorized cameras
if cam1isValid:
    cap = cv2.VideoCapture(camId1)
    width0 = cap.get(3)
    height0 = cap.get(4)
if cam2isValid:
    cap2 = cv2.VideoCapture(camId2)
    width1 = cap2.get(3)
    height1 = cap2.get(4)
if cam3isValid:
    cap3 = cv2.VideoCapture(camId3)
    width2 = cap3.get(3)
    height2 = cap3.get(4)


def update_cam_param():
    file = open("cam_param", "w") 
    file.write("c1=" + str(camId1) + "\n")
    file.write("c2=" + str(camId2) + "\n")
    file.write("c3=" + str(camId3) + "\n")
    file.write("END") 
    file.close()

    if cam1isValid:
        cap.release()
    if cam2isValid:
        cap2.release()
    if cam3isValid:
        cap3.release()

    os.execl(sys.executable, sys.executable, *sys.argv)



def callbackB1():
    camId1 = int(e.get())
    update_cam_param()
    
    #imprimer dans les params et restart

def callbackB2():
    camId2 = int(e2.get())
    update_cam_param()

def callbackB3():
    camId3 = int(e3.get())
    update_cam_param()


label = Label(cam1, text="Camera 1")
label.pack(side=LEFT)

e = Entry(cam1)
e.pack(side=LEFT)
b = Button(cam1, text="OK", command=callbackB1)
b.pack(side=LEFT)
e.insert(0, camId1)

label2 = Label(cam2, text="Camera 2")
label2.pack(side=LEFT)

e2 = Entry(cam2)
e2.pack(side=LEFT)
b2 = Button(cam2, text="OK", command=callbackB2)
b2.pack(side=LEFT)
e2.insert(0, camId2)
        
label3 = Label(cam3, text="Camera 3")
label3.pack(side=LEFT)

e3 = Entry(cam3)
e3.pack(side=LEFT)
b3 = Button(cam3, text="OK", command=callbackB3)
b3.pack(side=LEFT)
e3.insert(0, camId3)

imageLab = Label(cams)
imageLab.pack(side=LEFT)

imageLab2 = Label(cams)
imageLab2.pack(side=LEFT)

imageLab3 = Label(cams)
imageLab3.pack(side=LEFT)

states = LabelFrame(master, text="datas")
states.grid(row = 2, column = 0, rowspan = 2, columnspan = 1, sticky = W+E+N+S)

status = Label(states, text="Status : on hold\nConnected : Yes\nProgress : 0%\nDrawing : Line\nRemaining paint : 70%\n"
    + "")

status.pack(side=LEFT)

status2String = StringVar()

status2 = Label(states, textvariable=status2String)

status2String.set("Xt : {}; Yt : {}\nXe : {}; Ye : {}\na1 : {}°\n a2 : {}°\n a3 : {}°".format(xpos, 
    ypos, xposexp, yposexp, camangle1, camangle2, camangle3))

status2.pack(side=RIGHT)

can = Frame(master, bg="green")
can.grid(row = 0, column = 1, rowspan = 6, columnspan = 4, sticky = W+E+N+S)

footCan = Canvas(can, width=600, height=700, bg="green")

def update_text(gl1, gl2, gl3, p1, p2):
    status2String.set("Xt : {}; Yt : {}\nXe : {};\n Ye : {}\na1 : {}°\n a2 : {}°\n a3 : {}°".format(xpos, 
    ypos, p1, p2, gl1, gl2, gl3))

def _create_circle(x, y, r):
    return create_oval(x-r, y-r, x+r, y+r, fill="blue")

def coeff_from_angle(coeff, angl):
    angle_ = math.atan(coeff)
    angle_ = angle_ + angl
    return math.sin(angle_)/math.cos(angle_)


camState = False

#drawings of the lines depending on the file document
with open("terrain_data", "r") as ins:
    for line in ins:
        #faire du regex

        if line.split("[")[0] == "v":
            #it's a vector
            x1 = line.split("[")[1].split(";")[0]
            y1 = line.split("[")[1].split(";")[1]
            l1 = line.split("[")[1].split(";")[2]
            w1 = line.split("[")[1].split(";")[3].split("]")[0]
            
            footCan.create_line(x1, y1, int(x1)+int(l1), int(y1)+int(w1), fill="#fff")
            #print(x1, y1, x1+l1, y1+w1)

        elif line.split("[")[0] == "w":
            #it's a cam
            _id = int(line.split("[")[1].split(";")[0])
            print(_id)
            camposX[_id] = int(line.split("[")[1].split(";")[1])
            camposY[_id] = int(line.split("[")[1].split(";")[2].split("]")[0])

            footCan.create_oval(camposX[_id]-int(20), camposY[_id]-int(20), camposX[_id]+int(20), camposY[_id]+int(20), fill="red")

            if _id == 1 :
                camState = True

        elif line == "camangle":
            camangle = int(line.split("=")[1]) 

        if line == "end" :
            break;
        #print("test" + line)

if camState:

    angle = math.radians(-60)
    trianglex = int(math.cos(angle)*(camposX[1]-camposX[0]) - math.sin(angle)*(camposY[1] - camposY[0])+camposX[0])
    triangley = int(math.sin(angle)*(camposX[1]-camposX[0]) + math.cos(angle)*(camposY[1] - camposY[0])+camposY[0])

    footCan.create_oval(trianglex - int(20),triangley - int(20),trianglex + int(20),triangley + int(20), fill="red")

    camposX[2] = trianglex
    camposY[2] = triangley

    #don't forget to class the camera like 1 : top left, 2 : left-bottom & 3 : top-right

    #calcul des bissectrices (angle des bissectrices)
    director0to1 = -math.atan((camposY[1]-camposY[0])/(camposX[1]-camposX[0]))
    director1to2 = -math.atan((camposY[2]-camposY[1])/(camposX[2]-camposX[1]))
    director2to0 = -math.atan((camposY[0]-camposY[2])/(camposX[0]-camposX[2]))

    bisseX0 = (director0to1+director2to0)/2
    bisseX1 = (director1to2+director0to1)/2 + math.radians(90)
    bisseX2 = (director1to2+director2to0)/2


width, height = 160, 120

def show_robot(x, y):
    footCan.create_oval(x - int(10),y - int(10),x + int(10),y + int(10), fill="black")

footCan.pack()


def getColorTracking(raw_frame):

    frame_ = imutils.resize(raw_frame, width=600)
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)

    #s'occuper du color tracking

    hsv = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, redLower, redUpper)
    mask2 = cv2.inRange(hsv, redLower2, redUpper2)
    #mask = mask + mask2
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask


    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        angle = (camopenangle / width0) * x - (camopenangle/2)

        #use x and y as coord to find the angle
        cv2.putText(frame_, str(angle), (10, frame_.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame_, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame_, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    
    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 10 and i == 1 and pts[-10] is not None:

            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the
            # x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"

            # ensure there is significant movement in the
            # y-direction
            if np.abs(dY) > 20:
                dirY = "North" if np.sign(dY) == 1 else "South"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame_, pts[i - 1], pts[i], (0, 0, 255), thickness)


    #show the coords
    cv2.putText(frame_, "dx: {}, dy: {}".format(dX, dY), (10, frame_.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    frame_ = imutils.resize(frame_, width=width)

    return frame_, angle


def create_line_from_angle(x, y, angle):
    #draw the line with angle relative to the x (like in complex trigonometry)
    footCan.create_line(x, y, x + 2000, y - 2000*math.tan(math.radians(angle)), fill="#000")
    footCan.create_line(x, y, x - 2000, y + 2000*math.tan(math.radians(angle+180)), fill="#000")


def show_frame():

    #debugging
    #cam1isValid = True
    #cam2isValid = True
    #cam3isValid = True
    

    if cam1isValid :

        _, frame = cap.read()
        frameTracked, angle = getColorTracking(frame)

        cv2image = cv2.cvtColor(frameTracked, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        imageLab.imgtk = imgtk
        imageLab.configure(image=imgtk)
        

    else :

        #show dark image
        imageLab.imgtk = imageup
        imageLab.configure(image=imageup)

    if cam2isValid :

        _, frame2 = cap2.read()
        frameTracked2, angle2 = getColorTracking(frame2)

        #printing the cameras

        cv2image2 = cv2.cvtColor(frameTracked2, cv2.COLOR_BGR2RGBA)

        img2 = Image.fromarray(cv2image2)
        imgtk2 = ImageTk.PhotoImage(image=img2)
        imageLab2.imgtk = imgtk2
        imageLab2.configure(image=imgtk2)
        #imageLab2.after(10, show_frame)

    else:
        imageLab2.imgtk = imageup
        imageLab2.configure(image=imageup)

    if cam3isValid :

        _, frame3 = cap3.read()
        frameTracked3, angle3 = getColorTracking(frame3)

        #printing the cameras

        cv2image3 = cv2.cvtColor(frameTracked3, cv2.COLOR_BGR2RGBA)

        img3 = Image.fromarray(cv2image3)
        imgtk3 = ImageTk.PhotoImage(image=img3)
        imageLab3.imgtk = imgtk3
        imageLab3.configure(image=imgtk3)
        #imageLab3.after(10, show_frame)

    else:
        imageLab3.imgtk = imageup
        imageLab3.configure(image=imageup)

    imageLab.after(10, show_frame)
    

    #tout les updates dynamiques graphiques
    #-----------------------------------

    footCan.delete("all")
    #redraw everything
    footCan.create_oval(camposX[0]-int(20), camposY[0]-int(20), camposX[0]+int(20), camposY[0]+int(20), fill="red")
    footCan.create_oval(camposX[1]-int(20), camposY[1]-int(20), camposX[1]+int(20), camposY[1]+int(20), fill="red")
    footCan.create_oval(camposX[2]-int(20), camposY[2]-int(20), camposX[2]+int(20), camposY[2]+int(20), fill="red")

    #footCan.create_line(camposX[0], camposY[0], 500, 500*coeff_from_angle(bisseX1, math.radians(angle)), fill="#000")
    #footCan.create_line(camposX[0], camposY[0], 500, 500*bisseX1, fill="#000")
    camangle1 = float(angle)
    create_line_from_angle(camposX[0], camposY[0], math.degrees(director0to1))
    create_line_from_angle(camposX[1], camposY[1], math.degrees(director1to2))
    create_line_from_angle(camposX[2], camposY[2], math.degrees(director2to0))

    if cam1isValid:
        camangle1 = float(angle)
        create_line_from_angle(camposX[0], camposY[0], math.degrees(bisseX0)+camangle1)
    else:
        camangle1 = 0

    if cam2isValid:
        camangle2 = float(angle2)
        create_line_from_angle(camposX[1], camposY[1], math.degrees(bisseX1)+camangle2)
    else:
        camangle2 = 0

    if cam3isValid:
        camangle3 = float(angle3)
        create_line_from_angle(camposX[2], camposY[2], math.degrees(bisseX2)+camangle3)
    else:
        camangle3 = 0

    #----------------------------------------
    #calculer les intersections
    #first calculate droites equations
    
    camDroite[0][0] = math.tan(bisseX0 + math.radians(camangle1))
    camDroite[0][1] = -camposY[0] - math.tan(bisseX0 + math.radians(camangle1)) * camposX[0]

    camDroite[1][0] = math.tan(bisseX1 + math.radians(camangle2))
    camDroite[1][1] = -camposY[1] - math.tan(bisseX1 + math.radians(camangle2)) * camposX[1]

    camDroite[2][0] = math.tan(bisseX2 + math.radians(camangle3))
    camDroite[2][1] = -camposY[2] - math.tan(bisseX2 + math.radians(camangle3)) * camposX[2]

    #starting by inter 0-1, 1-2, 2-0
    xinter0et1 = (camDroite[1][1] - camDroite[0][1])/(camDroite[0][0] - camDroite[1][0])
    yinter0et1 = (camDroite[0][0] * camDroite[1][1] - camDroite[0][1] * camDroite[1][0])/(camDroite[0][0] - camDroite[1][0])

    xinter1et2 = (camDroite[2][1] - camDroite[1][1])/(camDroite[1][0] - camDroite[2][0])
    yinter1et2 = (camDroite[1][0] * camDroite[2][1] - camDroite[1][1] * camDroite[2][0])/(camDroite[1][0] - camDroite[2][0])

    xinter2et0 = (camDroite[0][1] - camDroite[2][1])/(camDroite[2][0] - camDroite[0][0])
    yinter2et0 = (camDroite[2][0] * camDroite[0][1] - camDroite[2][1] * camDroite[0][0])/(camDroite[2][0] - camDroite[0][0])

    #xposexp = (xinter0et1 + xinter1et2 + xinter2et0)/3
    #yposexp = (yinter0et1 + yinter1et2 + yinter2et0)/3

    #xposexp = math.fabs(xposexp)
    #yposexp = math.fabs(yposexp)

    xposexp = math.fabs(xinter0et1)
    yposexp = math.fabs(yinter0et1)

    show_robot(xposexp, yposexp)
    update_text(camangle1, camangle2, camangle3, xposexp, yposexp)



show_frame()

#toutes les données
'''avancement
tracer une ligne ou pas
connecté ou pas
peinture restante
Coords X et Y

'''

master.mainloop()
