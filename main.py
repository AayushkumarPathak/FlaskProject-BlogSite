from flask import *
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open("config.json", 'r') as c:
    params = json.load(c)['params']

local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER ='mail.gmail.com',
    MAIL_PORT = '465',
    MAIL_USERNAME =params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)
if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]

db = SQLAlchemy(app)

# Defining tables:-
'''
sno , name , phone_num , msg , date , email 
'''


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)
    msg = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(60), nullable=False)


@app.route("/")
def index():
    return render_template("index.html", params=params)


@app.route("/index")
def home():
    return render_template("home.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html", params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
                          sender=email,
                          recipients=[params['gmail-user']],
                          body =message+ "\n" +phone
                          )
    return render_template("contact.html", params=params)


@app.route("/post")
def post():
    return render_template("post.html", params=params)


app.run(debug=True)
