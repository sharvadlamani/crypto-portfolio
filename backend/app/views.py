from flask import Blueprint, request, jsonify
from .models import User as User
from . import db

main_bp=Blueprint('main',__name__)



@main_bp.route('/users',methods=['GET'])
def get_users():
    users=User.query.all()
    return jsonify([
       {'id':user.id,'username':user.username,'password':user.password, 'email':user.email} for user in users
    ])


