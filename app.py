import os
from flask import Flask, render_template, flash, redirect, url_for, request, json
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegistrationForm, HorseAdd, VideoAdd
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, relationship
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class



photos = UploadSet('photos', IMAGES)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
Bootstrap(app)
login = LoginManager(app)

login.login_view = 'login'
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bucbgleqiuhcxl:cecf4b39cf8e2363712a705d736ca3030dc2746cabe9160578e2e27e3e9c577f@ec2-54-247-85-251.eu-west-1.compute.amazonaws.com:5432/d2q067kt2tu8dd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG'])
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
configure_uploads(app, photos)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User %r>' % self.username
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Horse(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(128))
    info=db.Column(db.String)
    age= db.Column(db.Integer)
    Breeding= db.Column(db.String(128))
    price= db.Column(db.String(128))
  
   
    
    def __repr__(self):
        return '<Horse {}>'.format(self.name)  
     
        
class Image(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      photo = db.Column(db.String(128)) 
      horse_id = db.Column(db.Integer)
      def __repr__(self):
        return '<Image {}>'.format(self.photo)
    
class Video(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      video = db.Column(db.String(128)) 
      horse_id = db.Column(db.Integer)
      def __repr__(self):
        return '<Video {}>'.format(self.video)       
        
      

        
      
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
        
@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('add_horse'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('add_horse'))
    return render_template('login.html', title='Sign In', form=form)
    

@app.route("/", methods=['POST','GET'])

def index():
     images = Image.query.all()
   
     return render_template("index.html",images=images)

@app.route("/admin", methods=['POST','GET'])
@login_required
def add_horse():
    form=HorseAdd()
    filenames = []
    if request.method == 'POST':
            horse = Horse(name=form.name.data, age=form.age.data, Breeding=form.breeding.data,price=form.price.data,info=form.info.data)
            db.session.add(horse)
            db.session.flush()
            hid=horse.id
            db.session.commit()
            uploaded_files = request.files.getlist("file[]")
            for file in uploaded_files:
             
              if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Save the filename into a list, we'll use it later
                filenames.append(filename)
                
                image=Image(photo=filename, horse_id=hid)
                db.session.add(image)
                db.session.commit()
            return redirect(url_for('video',id=hid))
            
     
    return render_template("addhorse.html", form=form, filenames=filenames)

@app.route('/view/<id>')
def view(id):
    myhorse=Horse.query.get(id)
    images = Image.query.all()
    video = Video.query.all()
    return render_template("myhorse.html",myhorse=myhorse,id=id, images=images, video=video)
    
@app.route('/video/<id>',methods=['POST','GET'])
def video(id):
    form=VideoAdd()
    videoList= Video.query.all()
    if request.method == 'POST':
        video=Video(video=form.video.data,horse_id=id)
        db.session.add(video)
        db.session.commit()
        flash('video added')
    return render_template('addVideo.html', form=form, vids=videoList)
  
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)     

@app.route('/allhorses', methods=['POST','GET']) 
def allhorses():
    
        images=Image.query.all()
        return render_template("allhorses.html",images=images)


if __name__=='__main__':
    
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True
           )
    
    