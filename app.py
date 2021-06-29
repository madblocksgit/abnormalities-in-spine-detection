# -*- coding: utf-8 -*-

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
import tensorflow as tf

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='axial_model.h5'
MODEL_PATH1='sagital_model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model1 = load_model(MODEL_PATH1)

def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
   # x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    print(preds)
    if preds==0:
        preds="Normal"
    elif preds==1:
        preds="Abnormal"
    else:
        preds="Not Detected"
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('madhu.html')

@app.route('/axialpage')
def indexaxial():
    # Main page
    return render_template('index.html')
 
@app.route('/sagitalpage')
def indexsagital():
    # Main page
    return render_template('index1.html')

@app.route('/axial', methods=['GET', 'POST'])
def uploadaxial():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None

@app.route('/sagital', methods=['GET', 'POST'])
def uploadsagital():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model1)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(port=5001,debug=True)
