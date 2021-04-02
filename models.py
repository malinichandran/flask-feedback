
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()

bcrypt = Bcrypt()

def  connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    title = db.Column(db.String(100), 
                      nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username'))


class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), 
                         primary_key=True,
                         unique=True,
                         nullable=False)

    password = db.Column(db.Text,
                         nullable=False)

    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)

    firstname = db.Column(db.String(30),
                           nullable=False)

    lastname = db.Column(db.String(30),
                           nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls,username, pwd, email, fname, lname):
        """Register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email,
                    firstname=fname,lastname=lname)

    @classmethod
    def authenticate(cls, username, pwd):
        """Check if the user exists and if password is correct"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False


