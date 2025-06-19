from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, URL, ValidationError
from flask_ckeditor import CKEditorField

# Create a new blog post form
class AddBlogPost(FlaskForm):
    title = StringField(label="Blog title", validators=[DataRequired()])
    subtitle = StringField(label="Blog subtitle", validators=[DataRequired()])
    img_url = StringField(label="Background image url", validators=[DataRequired()])
    body = TextAreaField(label="Content", validators=[DataRequired()])
    submit = SubmitField(label='Submit')

# User registration form
class RegisterForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(),
                                                                           EqualTo("password",
                                                                                   message="Passwords must match")])
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField(label="Sign Up")

# User login form
class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


# Form to comment on posts
class CommentForm(FlaskForm):
    comment_text = TextAreaField("Comment", render_kw={"rows": 6}, validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
