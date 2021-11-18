from sqla_wrapper import SQLAlchemy
from sqlalchemy import ForeignKey
import os



db = SQLAlchemy(os.getenv("database_URL", "sqlite:///gtsn.sqlite"))
class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)

class Pontok(db.Model):
    __tablename__ = "Pontok"
    id = db.Column(db.Integer, primary_key=True)
    tippek = db.Column(db.Integer, unique=False)
    nehezseg = db.Column(db.String, unique=False)
    user = db.Column(db.Integer, ForeignKey("User.id"))

