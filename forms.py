from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField,HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
photos = UploadSet('photos', IMAGES)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class HorseAdd(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    breeding=StringField('Breeding', validators=[DataRequired()])
    age=StringField('Age', validators=[DataRequired()])
    info=TextAreaField('info')
    price=StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Add')

class VideoAdd(FlaskForm):
    horse_id=HiddenField("horse_id")
    video=StringField("video")
    submit = SubmitField('Add')