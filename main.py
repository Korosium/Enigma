# To load the environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Start of tutorial file
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        "author": "Korosium",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018"
    },
    {
        "author": "Korosium",
        "title": "Blog Post 2",
        "content": "First post content",
        "date_posted": "April 20, 2018"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True:
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)

def create_dummy_database():
    with app.app_context():
        # Reset the database
        db.drop_all()
        db.create_all()

        # Create the users
        user_1 = User(username="Koro", email="totally@legit.com", password="1234")
        db.session.add(user_1)
        db.session.commit()

        # Create the posts
        post_1 = Post(title="Blog 1", content="First Post Content!", user_id=user_1.id)
        post_2 = Post(title="Blog 2", content="Second Post Content!", user_id=user_1.id)
        db.session.add(post_1)
        db.session.add(post_2)
        db.session.commit()

if __name__ == "__main__":
    create_dummy_database()
    app.run(debug=True)