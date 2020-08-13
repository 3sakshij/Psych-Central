


from flask import Flask, render_template, flash, redirect, url_for, session, logging, request,flash
import MySQLdb
from flask_mysqldb import MySQL
from sqlalchemy.exc import IntegrityError

from sqlalchemy import create_engine
from passlib.hash import sha256_crypt
from sqlalchemy.orm import scoped_session ,sessionmaker
# import yaml
engine = create_engine("mysql+pymysql://root:sakshij30@localhost/register")
db =scoped_session(sessionmaker(bind =engine))
app = Flask(__name__)


# Configure db
# db = yaml.load(open('db.yaml'))
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

#mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            # Fetch form data
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']
            password = userDetails['password']
            password2 = userDetails['password2']
            secure_password = sha256_crypt.encrypt(str(password))



            if password ==password2:

                db.execute("INSERT INTO users(name, email,password) VALUES(:name,:email,:password )",
                           {"name":name ,"email":email,"password":secure_password})

                db.commit()
                flash("Registration successful log in to continue","Success")

                return render_template("index1.html")
            else:
                flash("Password does not match","danger")
                return render_template("index1.html")
    except IntegrityError:
        flash("Email already exist","danger")
        return render_template("index1.html")


    return render_template("index1.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password =request.form.get("password")

        emaildata = db.execute("select email from users where email = :email",{"email": email}).fetchone()
        pasworddata = db.execute("select password from users where email= :email",{"email":email}).fetchone()

        if emaildata is None:
            flash("NO such user exist", "danger")
            # return render_template("index1.html")
            return redirect("/")
        else:
            for password_data in pasworddata:
                if sha256_crypt.verify(password,password_data):
                    session['log'] = True
                    #flash("you are now loggin in ","success")
                    #return render_template("chatbot.html")
                    return redirect("/chat")
                else:
                    flash("Inncorrent password","danger")
                    # return render_template("index1.html")
                    return redirect("/")

    return render_template("index1.html")



@app.route('/chat')
def chat():
    return render_template("sucess1.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot1.html")

@app.route('/help')
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.secret_key = '12234556webcoding'
    app.run(debug =True)