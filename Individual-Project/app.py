from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyApZzDZSlsP57ae-epXKyWxf9K_WxA5FZI",
  "authDomain": "first-e71e8.firebaseapp.com",
  "databaseURL": "https://first-e71e8-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "first-e71e8",
  "storageBucket": "first-e71e8.appspot.com",
  "messagingSenderId": "187746478309",
  "appId": "1:187746478309:web:2e462a6e5370414c8a4c0c",
  "measurementId": "G-K68685HPFJ",
  "databaseURL": "https://first-firebase-ff06e-default-rtdb.firebaseio.com/"


}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("yo")
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"name": request.form['full_name'], "email":request.form['email'], "username": request.form["username"], "password": request.form["password"]}
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('add'))
		        
		  
        error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form["date"]
        text = request.form["text"]
        uid = db.child("Users").child(login_session['user']['localId']).get().val()
        
        #try:
        add = {"date": date, "text": text, "uid": uid}
        db.child("Page").push(add)
        

        return redirect(url_for('all'))
        #except:
        print("Couldn't add page")
        return render_template("add.html")
    return render_template("add.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))
    
@app.route('/all', methods = ['GET', 'POST'])
def all():
    add = db.child("Page").get().val()


    return render_template("all.html", t = add)
if __name__ == '__main__':
    app.run(debug=True)