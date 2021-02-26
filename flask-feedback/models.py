from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    '''User model for making a user'''
    __tablename__='users'
    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='user', cascade='all,delete')

    @classmethod
    def register(cls, un, pw, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pw)
        hashed_utf8 = hashed.decode('utf8')
        new_user = cls(username=un, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, un, pw):
        '''validate that user exists and password matches
        return user if valid, else return False'''
        u=User.query.filter_by(username=un).first()
        if u and bcrypt.check_password_hash(u.password, pw):
            return u
        else:
            return False

class Feedback(db.Model):
    '''Model for creating feedback'''
    __tablename__='feedback'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(),
        db.ForeignKey('users.username'),
        nullable=False,
    )

def connect_db(app):
    db.app = app
    db.init_app(app)