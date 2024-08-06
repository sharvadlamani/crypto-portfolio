from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User as User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
from flask_login import current_user



auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data=request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                message={'message':'Logged in successfully!', "category":'success'}
                login_user(user, remember=True)
                return jsonify(message,201)
            else:
                message={'message':'Incorrect password, try again.', "category":'error'}
                return jsonify(message,201)
        else:
            message={'message':'Username does not exist.', "category":'error'}
            return jsonify(message,201)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    message={'message':'User logged out', "category":'success'}
    return jsonify(message,201)

@auth_bp.route('/isloggedin', methods=['GET'])
def isloggedin():
    if current_user.is_authenticated:
        message= {'message': 'is logged', "category":'success'}
    else:
        message={'message':'not logged', "category":'error'}
    return jsonify(message),201

@auth_bp.route('/currentuserdetails', methods=['GET'])
@login_required
def currentuserdetails():
    message={
        'message':{
            'username':current_user.username,
            'email':current_user.email
        },
        'category':'success'
    }
    return jsonify(message),201



@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data=request.get_json()
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        user = User.query.filter_by(email=email).first()
        message={}
        if user:
            message={'message':'Email already exists.', "category":'error'}
        elif len(email) < 4:
            message={'message':'Email must be greater than 3 characters.', "category":'error'}
        elif len(username) < 2:
            message={'message':'Username must be greater than 1 character.', "category":'error'}
        elif password1 != password2:
            message={'message':'Passwords don\'t match.', "category":'error'}
        elif len(password1) < 7:
            message={'message':'Password must be at least 7 characters.', "category":'error'}

        else:
            try:
                user=User.query.filter_by(username=username).first()
                if user:
                    message={'message':'Username already exists.', "category":'error'}
                    return jsonify(message,201)
            except:
                pass
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            #flash('Account created!', category='success')
            message={'message':'account created', "category":'success'}
            return jsonify(message,201)
            #return redirect(url_for('views.home'))

    return jsonify(message,201)