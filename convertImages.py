#This script convertes images of different sizes to an uniform size, with possibility to convert them to gray scale
#Opencv3 is necessary, download and install it as described in this tutorial:
#http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
import cv2
import os
from os import walk
import sys


#Parameters
src = "imgconv/roof_images"
dest = "imgconv/roof_images_c"
#Constants
GRAYSCALE = False
WIDTH = 32
HEIGHT = WIDTH

#Test if the source is correct
if not os.path.exists(src):
    print "Source directory not found"
    exit()

#Test if destination folder exists, if not create it
if not os.path.exists(dest):
    os.makedirs(dest)

#Read all the files in the directory
f = []
for (dirpath, dirnames, filenames) in walk(src):
    f.extend(filenames)
    break
print "Converting images..."
i = 0
#For each file:
for picture in f:
    #We want only jpg files in this script to be converted
    if picture.endswith(".jpg"):
        #Check for bad endings
        if not src.endswith("/"):
            src = src + "/"
        if not dest.endswith("/"):
            dest = dest + "/"
        
        img = cv2.imread(src + picture)
        if GRAYSCALE:
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            res = cv2.resize(gray,(WIDTH, HEIGHT), interpolation = cv2.INTER_CUBIC)
        else:
            res = cv2.resize(img,(WIDTH, HEIGHT), interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(dest+ picture,res)
        i = i+1
        if i % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
    else:
        print picture +" is not an image!"
print ""
print "Conversion done!"
