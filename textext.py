#Fyle date extraction assignment

import cv2
import numpy as np
import pytesseract
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pytesseract import image_to_string
import os
import re

src_path = "/home/keerthi/Downloads/Receiptssmall/"
data_paths = [i for i in (os.path.join(src_path, f) for f in os.listdir(src_path)) if os.path.isfile(i)]
#print(data_paths)

def get_string(img_path):

    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    cv2.threshold(cv2.GaussianBlur(img,(5,5),0),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    #cv2.imwrite(src_path , img)
    #cv2.imwrite(src_path + "thres.png", img)
    result = pytesseract.image_to_string(Image.open(img_path ))

    return result
#print(get_string(src_path))
k=0
l=[]
j=1
for i in data_paths:
    print(j)
    l.append(get_string(i))
    j+=1

#-----------------------RegEx---------------------------------------------------

count=0
for j in l:
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', j)
    match1 = re.search(r'(\d{1,2}-\d{1,2}-\d{4})',j)
    match2 = re.search(r'(\d{1,2}-\d{1,2}-\d{2})',j)
    match3 = re.search(r'(\d{1,2}/\d{1,2}/\d{2})', j)
    match4 = re.search(r'([\d]{1,2}/[ADFJMNOS]\w*/[\d]{4})',j)
    match5 = re.search(r'([\d]{1,2}/[ADFJMNOS]\w*/[\d]{2})',j)
    match6 = re.search(r'([\d]{1,2}-[ADFJMNOS]\w*-[\d]{4})',j)
    match7 = re.search(r'([\d]{1,2}-[ADFJMNOS]\w*-[\d]{2})',j)
    if(match):

        i=match.group(1)
        i=i.split("/")
        if(i[-1]>'2019' or (i[1] > '31' )):
        	count+=1
        	continue
        else:
        	print(match.group(1))
        	count+=1
    elif(match1):
    	i=match1.group(1)
    	i=i.split("-")
    	if(i[-1]>'2019' or (i[1] > '31' )):
    		count+=1
    		continue
    	else:
    		print(match1.group(1))
    		count+=1

    elif(match2):
    	i=match2.group(1)
    	i=i.split("-")
    	if(i[-1]>'2019' or (i[1] > '31' )):
    		count+=1
    		continue
    	else:
    		print(match2.group(1))
    		count+=1
    elif(match3):
    	i=match3.group(1)
    	i=i.split("/")
    	if(i[-1]>'2019' or (i[1] > '31' )):
    		count+=1
    		continue
    	else:
    		print(match3.group(1))
    		count+=1
    elif(match4):
    	print(match4.group(1))
    	count+=1
    elif(match5):
    	print(match5.group(1))
    	count+=1
    elif(match6):
    	print(match6.group(1))
    	count+=1
    elif(match7):
    	print(match7.group(1))
    	count+=1
    else:
    	print("Null")
    	
    k+=1



print((count/len(l))*100.00)
