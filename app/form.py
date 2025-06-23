from flask_wtf import FlaskForm 
from flask_wtf.file import FileField ,FileAllowed 
from wtforms import StringField, SubmitField, PasswordField ,TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo ,ValidationError
from app.models.userdb import User
from flask_login import current_user

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_name(self , name):
        user = User.query.filter_by(username =name.data).first()
        if user:
            raise ValidationError(' This name is Taken Plz Select another one.') 
        
    def validate_email(self , email):
        user = User.query.filter_by(email =email.data).first()
        if user:
            raise ValidationError(' This email is Taken Plz Select another one.')       

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign-In')

class UpdateAccountForm(FlaskForm):
    name = StringField('New Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('New Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Select a Profile Image' , validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_name(self , name):
        if current_user.username != name.data:
            user = User.query.filter_by(username =name.data).first()
            if user:
                raise ValidationError(' This name is Taken Plz Select another one.') 
        
    def validate_email(self , email):
        if current_user.email != email.data:
            user = User.query.filter_by(email =email.data).first()
            if user:
                raise ValidationError(' This email is Taken Plz Select another one.')
            

class CreatePostForm(FlaskForm):
    title = StringField('Enter Your Title', validators=[DataRequired()])
    content = TextAreaField('Write your Content', validators=[DataRequired()])
    submit = SubmitField('Post It')