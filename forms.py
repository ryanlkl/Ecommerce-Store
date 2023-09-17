from wtforms import StringField, FloatField, SubmitField, EmailField, PasswordField, TextAreaField, FileField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  email = EmailField("Email",validators=[DataRequired()])
  password = PasswordField("Password",validators=[DataRequired()])
  submit = SubmitField("Login")

class RegisterForm(FlaskForm):
  first_name = StringField("First Name",validators=[DataRequired()])
  last_name = StringField("Last Name",validators=[DataRequired()])
  email = EmailField("Email",validators=[DataRequired()])
  password = PasswordField("Password",validators=[DataRequired()])
  submit = SubmitField("Sign Up")

class CreateProductForm(FlaskForm):
  title = StringField("Product Name",validators=[DataRequired()])
  price = FloatField("Price",validators=[DataRequired()])
  description = CKEditorField("Product Description",validators=[DataRequired()])
  categories = TextAreaField("Categories", validators=[DataRequired()])
  img_url = FileField("Images", validators=[DataRequired()])
  submit = SubmitField("Create")

class ReviewForm(FlaskForm):
  pass
