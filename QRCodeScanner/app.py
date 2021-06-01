from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image
import io
from pyzbar.pyzbar import decode

app = Flask(__name__)



def decodeImg(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        
        print("Barcode: "+barcodeData +" | Type: "+barcodeType)
        return barcodeData


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        filename =request.files['filename'].read()
        img = (np.array(Image.open(io.BytesIO(filename))) )
        cv2.imshow("img",img)
        data = decodeImg(img)
    return render_template('result.html', finalResult = data)