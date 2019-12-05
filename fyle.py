import os
from flask import Flask, render_template, request
import cv2
import numpy as np
import pytesseract
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pytesseract import image_to_string
import os
import re
#from ocr_core import ocr_core

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

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
	result = pytesseract.image_to_string(Image.open(img_path ))
	return result
def extract_date(j):
	c=0
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
			c+=1
			#continue
		else:
			k=match.group(1)
	elif(match1):
		i=match1.group(1)
		i=i.split("-")
		if(i[-1]>'2019' or (i[1] > '31' )):
			c+=1
			#continue
		else:
			k=match1.group(1)
	elif(match2):
		i=match2.group(1)
		i=i.split("-")
		if(i[-1]>'2019' or (i[1] > '31' )):
			c+=1
			#continue
		else:
			k=match2.group(1)
	elif(match3):
		i=match3.group(1)
		i=i.split("/")
		if(i[-1]>'2019' or (i[1] > '31' )):
			c+=1
			#continue
		else:
			k=match3.group(1)
	elif(match4):
		k=match4.group(1)
	elif(match5):
		k=match5.group(1)
	elif(match6):
		k=match6.group(1)
	elif(match7):
		k=match7.group(1)
	else:
		k='Null'
	return k

def ocr_core(fname):
	l=[]
	l.append(get_string(i))
	k=extract_date(l[0])
	return k

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(UPLOAD_FOLDER+file.filename)

            # call the OCR function on it
            extracted_text, Date = ocr_core(file)
            # extract the text and display it
            return render_template('upload.html',msg='Successfully processed',extracted_text=extracted_text,extracted_date = Date,img_src= file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run("0.0.0.0","4500")
