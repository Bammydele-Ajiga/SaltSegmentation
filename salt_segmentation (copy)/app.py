
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from main import get_pred
import os
from skimage.io import imread, imshow
from PIL import Image
import numpy as np

#Save images to the 'static' folder as Flask serves images from this directory
UPLOAD_FOLDER = 'static/images/'

#Create an app object using the Flask class. 
app = Flask(__name__, static_folder="static")


app.secret_key = "secret key"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

#Add Post method to the decorator to allow for form submission. 
@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)  #Use this werkzeug method to secure filename. 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            filename =os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #getPrediction(filename)
            res = get_pred(filename)
            # flash(res)
            res = Image.fromarray((res* 255).astype(np.uint8))
            basewidth = 300
            wpercent = (basewidth/float(res.size[0]))
            hsize = int((float(res.size[1])*float(wpercent)))
            img = res.resize((basewidth,hsize), Image.ANTIALIAS)
            img.save("static/images/result.png")
            # plt.savefig()
            # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "result.png")
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            return redirect('/')


if __name__ == "__main__":
    app.run()
