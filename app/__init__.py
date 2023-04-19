from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import create_engine
from flask_mail import Mail, Message

##########################################################################3

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'handswash2@gmail.com', 
	MAIL_PASSWORD = 'csbtokeuhwbtuahu'	
	)
 
##########################################################################3

dirname = os.path.abspath(os.path.dirname(__file__))

app.secret_key = 'myonwayisskyonway'

#app.config['SQLALCHEMY_DATABASE_URI'] = 



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db_string = 'postgres://aljuvqkgojhfjn:32251d686e5c64cf5af5c545e156e07c86ed72a0cdb6a573c54878a90fc2e90e@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d904lrr6enfblk'
#db_string = 'sqlite:///' + os.path.join(dirname, 'db.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = db_string

db = create_engine(db_string)

mb=  SQLAlchemy(app)

ma = Marshmallow(app)

from app import final2

#########################################################################