import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from dotenv import load_dotenv
import os
load_dotenv()

# database_path = os.getenv('DATABASE_URL')

# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)
database_path = "postgresql://postgres_deployment_example_60m2_user:xq0knbOVJUe5gdKUy6xmMhWPYsWhJ20J@dpg-ctodvj52ng1s73biauk0-a/postgres_deployment_example_60m2"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}
