from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key="somethingsecretIcannotthinkofsmthbruh"
app.permanent_session_lifetime = timedelta(days=7)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER ="static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email =db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False )
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(300), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/market")
def market():
    if "user" not in session:
        return redirect(url_for("signin"))
    
    user = User.query.filter_by(email=session["user"]).first()
    return render_template("market.html", user=user)

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    if "user" not in session:
        return redirect(url_for("signin"))
    
    user = User.query.filter_by(email=session["user"]).first()

    if request.method =="POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")

        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )

        new_post = Post(
            title=title,
            description=description,
            price=float(price),
            image=filename,
            user_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('profile'))
    
    return render_template("add_post.html")

@app.route("/register", methods=["GET", "POST"] )
def register():
   if request.method == "POST":
    name= request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return"User already exists"
    
    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session.permanent = True
    session["user"] = email

    return redirect(url_for("market"))
   

   return render_template("register.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.permanent = True
            session["user"] = email
            return redirect(url_for("market"))
        
        return "Invalid Login Details"
    return render_template("signin.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email=session["user"]).first()

    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template("profile.html", user=user, posts=posts)

@app.route("/order")
def order():
    if "user" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email=session["user"]).first()
    return render_template("orders.html")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("signin"))

@app.route("/checkout")
def chechout():
    if "user" not in session:
        return redirect(url_for("signin"))
    user = User.query.filter_by(email=session["user"]).first()
    return render_template("checkout.html")

@app.route("/shop")
def shop():
    if "user" not in session:
        return redirect(url_for("signin"))
    user=User.query.filter_by(email=session["user"]).first()
    return render_template("shop.html")

if __name__ == "__main__":
   app.run(debug=True)
