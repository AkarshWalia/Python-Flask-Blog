from flask import Blueprint ,redirect ,url_for,render_template,flash,request
from app.form import RegisterForm ,SignInForm
from app.routes.main_bp import home
from app import bcrypt , db
from app.models import User
from flask_login import login_user ,current_user , logout_user 

auth = Blueprint('auth',__name__)

@auth.route('/register' , methods = ['POST' ,'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.name.data , email = form.email.data , password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfuly . SignIn Please ' , 'success')
        return redirect(url_for('auth.signIn'))
    
    return render_template('register.html',form = form)

@auth.route('/signIn' , methods = ['POST' ,'GET'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password ,form.password.data):
            login_user(user)
            next_page =request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsucessful check email or password' )
        
    return render_template('signin.html',form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.register'))