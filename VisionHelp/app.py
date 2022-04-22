
from flask import Flask, render_template, request, redirect, url_for

import cv2
import numpy as np

import base64
import io
from PIL import Image

import os

#import rds_db as db


app = Flask(__name__)

@app.route('/')
def userInfo():
    return render_template('UserInfo.html')

@app.route('/instructions')
def display_inst():
    return render_template('Instructions.html')

@app.route('/Hypermetropia')
def myopia_quiz():
    return render_template('Hypermetropia.html')
    
@app.route('/testchoice')
def display_test_choices():
    return render_template('testChoice.html')

@app.route("/hypermetropia")
def display_hypeprmetropia():
    return render_template("hypermetropia.html")
#@app.route('/')
#def home_page():
#    return render_template('home_page.html')

#@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global username
    # if we get a form request to log in
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['password']
        try:
            user_id = db.get_user(username, password)
            print("user logged in succesesfully")
            # if valid user_id, reroute to landing page of user
            # return render_template('landing.html',variable=username)
            return render_template('landing.html',variable=username)
        except Exception as e:
            return render_template('login.html', var=e)
    return render_template('login.html')

#@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    # if we get a form request to sign up
    global username
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']
        # call db function
        try:
            user_id = db.insert_new_user(username, email, password, confirm_password)
        except Exception as e:
            return render_template('signup.html', var=e)
        return render_template('landing.html', variable=username)
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('upload_image.html')
    if request.method == 'POST':
        img_bs64 = request.form['canvas_datauri'].split(',')[1]
        # print(request.form['canvas_datauri'][:40].split(',')[1])

        im_binary = base64.b64decode(img_bs64)
        buf = io.BytesIO(im_binary)
        img = Image.open(buf)

        img.save("./static/images/farImg.png", format="png")

        context = dict()
        context['message'] = "Successfully uploaded - Go to next page -  Just a message"
        return render_template('upload_image.html', content = context)


@app.route('/blur', methods=['GET', 'POST'])
def blur_image():
    if request.method == 'GET':
        if not os.path.exists('./static/images/blurs/1.png') or not os.path.exists('./static/images/blurs/2.png') or not os.path.exists('./static/images/blurs/3.png'):
            # generate blurred and save - Check if farImg is present
            baseImg = cv2.imread('./static/images/farImg.png')
            iterImg = baseImg

            # Blurs
            for i in range(3):
                bluri = blurAndSave(iterImg, i+1)
                iterImg = bluri

        return render_template('blur.html')

# main driver function
if __name__ == '__main__':
    app.run()


# if __name__ == "__main__":
#     app.run(ssl_context='adhoc')

def blurAndSave(img, i):
    blur = cv2.blur(img, (i*i, i*i))
    cv2.imwrite(f'./static/images/blurs/{i}.png', blur)
    return blur
