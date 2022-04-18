
from flask import Flask, render_template, request, redirect, url_for
#import rds_db as db
  

app = Flask(__name__)

@app.route('/')
def userInfo():
    return render_template('UserInfo.html')

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

# main driver function
if __name__ == '__main__':
    app.run()