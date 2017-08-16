# Creates an enhanced dataset, with rotated images. Was used for the Data Science Game 2016 where roofs had to be classified.
# https://inclass.kaggle.com/c/data-science-game-2016-online-selection
# Requires opencv, check for installation:
#http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/

import numpy as np
import cv2
import csv

MEAN = 0
STDEV = 10

def add_random_noise(img):
    (h, w) = img.shape[:2]
    noise = np.zeros((h, w, 3))
    return img + cv2.randn(noise,  MEAN,  STDEV)
    
def transform_image(img,  vertical_flip,   horizontal_flip,  rotation):
    (h, w) = img.shape[:2]
    center = (w/2,  h/2)
    if vertical_flip:
        img = cv2.flip(img, 1)
    if horizontal_flip:
        img = cv2.flip(img, 0)
    if rotation is not 0:
        M = cv2.getRotationMatrix2D(center,  rotation,  1.0)
        img = cv2.warpAffine(img,  M,  (w, h))
    img = add_random_noise(img)
    h = int(h * (1.0 + (np.random.rand())/10.0))
    w = int(w * (1.0 + (np.random.rand())/10.0))
    img = cv2.resize(img,(h, w), interpolation = cv2.INTER_CUBIC)
    return img

src = "imgconv/roof_images/"
dest = "imgconv/roof_enhanced/"
imgnames = []
rawlabels = []
skip = ["-1311082"]

print("Reading csv")
with open('id.train.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for line in csvreader:
        imgnames.append(line[0])
        rawlabels.append(line[1])

print("Converting images")

for i in xrange(len(imgnames)):
#for i in xrange(100):
    name = imgnames[i]
    ending = ".jpg"
    img = cv2.imread(src + name + ending)
    #Do transformations
    img90 = transform_image(img,  False,  False,  90)
    img180 = transform_image(img,  False,  False,  180)
    img270 = transform_image(img,  False,  False,  270)
    imgv = transform_image(img,  True,  False,  0)
    imgv90 = transform_image(img,  True,  False,  90)
    imgv180 = transform_image(img,  True,  False,  180)
    imgv270 = transform_image(img,  True,  False,  270)
    if int(rawlabels[i]) is 1: #nord south orientation
        #Write them to the disk
        destimg = dest + "1/"
        cv2.imwrite(destimg+ name + "" + ending,img)
        cv2.imwrite(destimg+ name + "_180" + ending,img180)
        cv2.imwrite(destimg+ name + "_v" + ending,imgv)
        cv2.imwrite(destimg+ name + "_v180" + ending,imgv180)
        destimg = dest + "2/"
        cv2.imwrite(destimg+ name + "_90" + ending,img90)
        cv2.imwrite(destimg+ name + "_270" + ending,img270)
        cv2.imwrite(destimg+ name + "_v90" + ending,imgv90)
        cv2.imwrite(destimg+ name + "_v270" + ending,imgv270)
    elif int(rawlabels[i]) is 2: #east west orientation
        #Write them to the disk
        destimg = dest + "2/"
        cv2.imwrite(destimg+ name + "" + ending,img)
        cv2.imwrite(destimg+ name + "_180" + ending,img180)
        cv2.imwrite(destimg+ name + "_v" + ending,imgv)
        cv2.imwrite(destimg+ name + "_v180" + ending,imgv180)
        destimg = dest + "1/"
        cv2.imwrite(destimg+ name + "_90" + ending,img90)
        cv2.imwrite(destimg+ name + "_270" + ending,img270)
        cv2.imwrite(destimg+ name + "_v90" + ending,imgv90)
        cv2.imwrite(destimg+ name + "_v270" + ending,imgv270)
    elif int(rawlabels[i]) is 3: #flat roof
        #Write them to the disk
        destimg = dest + "3/"
        cv2.imwrite(destimg+ name + "" + ending,img)
        cv2.imwrite(destimg+ name + "_180" + ending,img180)
        cv2.imwrite(destimg+ name + "_v" + ending,imgv)
        cv2.imwrite(destimg+ name + "_v180" + ending,imgv180)
        cv2.imwrite(destimg+ name + "_90" + ending,img90)
        cv2.imwrite(destimg+ name + "_270" + ending,img270)
        cv2.imwrite(destimg+ name + "_v90" + ending,imgv90)
        cv2.imwrite(destimg+ name + "_v270" + ending,imgv270)
    elif int(rawlabels[i]) is 4: #other
        #Write them to the disk
        destimg = dest + "4/"
        cv2.imwrite(destimg+ name + "" + ending,img)
        cv2.imwrite(destimg+ name + "_180" + ending,img180)
        cv2.imwrite(destimg+ name + "_v" + ending,imgv)
        cv2.imwrite(destimg+ name + "_v180" + ending,imgv180)
        cv2.imwrite(destimg+ name + "_90" + ending,img90)
        cv2.imwrite(destimg+ name + "_270" + ending,img270)
        cv2.imwrite(destimg+ name + "_v90" + ending,imgv90)
        cv2.imwrite(destimg+ name + "_v270" + ending,imgv270)
        
    if i % 100 == 0:
        print("At step " + str(i) + " of " + str(len(imgnames)))
