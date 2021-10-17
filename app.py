from enum import unique
from operator import add, eq
from flask import Flask, redirect,request, render_template,session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import CharsetAccept
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
from mysql import connector



app=Flask(__name__, template_folder='templets')
app.secret_key='sathi'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class chat(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column('name',db.String(100))
    email=db.Column('email',db.String(100),unique=True)
    number=db.Column('number',db.String(100))
    password=db.Column('password',db.String(100))
    def __init__(self,name,email,number,password):
        self.name=name
        self.email=email
        self.number=number
        self.password=password
    def is_active(self):
        return True

login_manager= LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return chat.query.get(int(id))


@app.route('/', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=chat.query.filter_by(email=email).first()
        pas=chat.query.filter_by(password=password).first()
        
        if user :
            if pas :
                flash('Login successfull')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('incorrect login, try again')
                
        else:
            flash('user not exist Create your account')
            return redirect(url_for('signup'))


    
    return render_template('login.html', users=current_user)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', users=current_user)

@app.route('/signup', methods=['GET','POST','DELETE'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        name=request.form['name']
        number=request.form['number']
        pass1=request.form['password']
        pass2=request.form['password1']
        user=chat.query.filter_by(email=email).first()
        if len(name)<2:
            flash('name must be > 2')
        elif len(email)<4:
            flash('email Too Short. Must be > 4')
        elif len(number)!=10:
            flash('Enter Valid Number')
        elif 15 > len(pass1)<7:
            flash('password must be b/w 7-15')
        elif pass1!=pass2:
            flash('passwords not matching')
        
        
        else:   
            if user:
                flash('this email already exist ! login here')
                return redirect(url_for('login'))
            

            flash('Signup Success',category='success')
            add_items=chat(name,email,number,pass1)
            db.session.add(add_items)
            db.session.commit()
            
            return redirect(url_for('login'))
    
         
            
        
        
    return render_template('signup.html', users=current_user)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
