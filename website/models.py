from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Course')
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(6))
    term = db.Column(db.String(20), default="202408")
    seats_available = db.Column(db.Integer,default=-1)
    course_name = db.Column(db.String(15))
    course_info = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    
