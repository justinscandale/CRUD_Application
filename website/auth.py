from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Course
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category = 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home',user=user))
            else:
                flash('Incorrect password, try again', category = 'error')
        else:
            flash('Email does not exsist', category= 'error')
    return render_template("login.html", user = "Bob", text = "Passed String")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exsists", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email,password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created', category='success')
            login_user(new_user, remember=True)
            new_course1 = Course(data="00000", seats_available= 10, course_name = "Example", course_info = "Ex 101", user_id=current_user.id, term="202405")
            new_course2 = Course(data="00001", seats_available= 0, course_name = "Example", course_info = "Ex 202", user_id=current_user.id, term="202408")
            db.session.add(new_course1)
            db.session.add(new_course2)
            db.session.commit()
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html",user = current_user)


