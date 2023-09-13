from flask import Flask, render_template, redirect, url_for, abort, flash, request
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy.orm import relationship
import os
from flask_ckeditor import CKEditor
from forms import LoginForm, RegisterForm, ReviewForm, CreateProductForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecom.db"
db = SQLAlchemy()
db.init_app(app)

# Configure tables
class Product(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.Text, nullable=False)
  img_url = db.Column(db.String(250), nullable=False)
  reviews = relationship("Review", back_populates="parent_product")

class User(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  first_name = db.Column(db.String(20), nullable=False)
  last_name = db.Column(db.String(20), nullable=False)
  reviews = relationship("Review", back_populates="review_author")

class Review(db.Model):
  __tablename__ = "reviews"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  text = db.Column(db.Text, nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
  parent_product = relationship("Product",back_populates="reviews")
  review_author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  review_author = relationship("User", back_populates="reviews")

with app.app_context():
  db.create_all()

# admin-only decorator
def admin_only(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if current_user.email != "admin@eccom.com":
      return abort(403)
    return f(*args,**kwargs)

  return decorated_function


# Website routes

@app.route("/")
def home():
  print("home")
  return render_template("index.html")

@app.route("/sign-in", methods=["GET","POST"])
def sign_in():
  register_form = RegisterForm()
  login_form = LoginForm()
  if register_form.validate_on_submit():

    user = db.session.execute(db.select(User).where(User.email == register_form.email.data)).scalar()
    if user:
      flash("You've already signed up with that email, log in instead.")
      return redirect("sign-up")

    password = generate_password_hash(
      register_form.password.data,
      method = 'pbkdf2:sha256',
      salt_length = 8
    )
    new_user = User(
      first_name = register_form.first_name.data,
      last_name = register_form.last_name.data,
      email = register_form.email.data,
      password = password
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for("home"))

  if login_form.validate_on_submit():
    password = login_form.password.data
    user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
    if not user:
      flash("That email does not exist, please try again.")
      return redirect(url_for("sign-in"))
    elif not check_password_hash(user.password, password):
      flash("Password incorrect, please try again.")
      return redirect(url_for("sign-in"))
    else:
      login_user(user)
      return redirect(url_for("home"))

  return render_template("sign-in.html", register_form = register_form, login_form = login_form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))

@app.route("/men")
def men():
  return render_template("men.html")


if __name__ == "__main__":
  app.run(debug=True)
