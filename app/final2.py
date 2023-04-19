# importing libraries
from app import app
from flask import request, jsonify, render_template , flash, redirect , url_for
from app import mb
from app import ma
from app import db
from datetime import datetime
import pytz
from flask_mail import Mail, Message
import requests
from random import randint

mail = Mail(app)

################################################################

# creates table after opening webpage first time.
@app.before_first_request
def create_tables(): 
    mb.create_all()

####################################################################

# creating database table product
class product(mb.Model):
	id = mb.Column(mb.Integer(), primary_key = True)
	name = mb.Column(mb.String(30))
	em = mb.Column(mb.String(30))
	dbs = mb.Column(mb.String(30))

	def __init__(self,name, em, dbs):
		self.name = name
		self.em = em 
		self.dbs = dbs


########################################################

# creating table tmp in database
class tmp(mb.Model):
	id = mb.Column(mb.Integer(), primary_key = True)
	usrnm = mb.Column(mb.String(120))
	ema = mb.Column(mb.String(100))
	dbs = mb.Column(mb.String(100))
	rand = mb.Column(mb.Integer())

	def __init__(self, usrnm, ema, dbs, rand):
		self.usrnm = usrnm
		self.ema = ema 
		self.dbs = dbs
		self.rand = rand		


###########################################################3

# creating productSchema that will used if it is used as REST API as well.
class productSchema(ma.Schema):
	class Meta:
		fields = ('id', 'currentDate', 'currentTime','latitude', 'longitude', 'accuracy')


product_schema = productSchema()
products_schema = productSchema(many = True)

##################################################################

# home page
@app.route('/')
def home():
	return render_template("home.html")

####################################################################

# view page
@app.route('/view/<name>')
def view(name):
	result_set = db.execute("SELECT * FROM {}".format(name))
	return render_template("view.html", values = result_set)


##################################################################

# handle JSON data if comes from POST request
@app.route('/usingson', methods = ['POST'])
def example():
	data = request.get_json()
	
	latitude = data['latitude']
	longitude = data['longitude']
	accuracy = data['accuracy']

	new_data = product(latitude, longitude, accuracy)
	db.session.add(new_data)
	db.session.commit()

	return '''<h1> The latitude is : {}
				   The longitude is : {}
				   The accuracy is : {}</h1>'''.format(latitude, longitude, accuracy)



##############################################################################


# This is main function or route used to insert data in to database via 'urlencoded technique'
@app.route('/query_example', methods= ['GET'])
def query_example():
	now = datetime.now()
	tz = pytz.timezone('Asia/Kolkata')
	your_now = now.astimezone(tz)
	currentTime = your_now
	currentTime = your_now.strftime("%H:%M:%S")
	currentTime = str(currentTime)
	#now = datetime.now()
	currentDate = your_now.strftime("%d/%m/%Y")
	currentDate = str(currentDate)
	#currentTime = now.strftime("%H:%M:%S")
	stm = request.args.get('kts')
	stm = str(stm)
	Latitude = request.args.get('latitude')
	Latitude = str(Latitude) 
	Longitude = request.args.get('longitude')
	Longitude = str(Longitude)
	Accuracy = request.args.get('accuracy')
	Accuracy = str(Accuracy)

	
	db.execute("INSERT INTO {} (currtime, currdate, latitude, longitude, accuracy) VALUES ('{}', '{}', '{}', '{}', '{}')".format(stm, currentTime, currentDate, Latitude, Longitude, Accuracy))

	return "<h1> submitted </h1"


###################################################################################################

# to get data which printed on webpage if anyone is login there after signup....
@app.route('/gtb', methods=["POST"])
def gtb():
	if request.method == 'POST':
		uer = request.form["usrsnm"]
		bts = request.form["btsname"]

		found_user = product.query.filter_by(name=uer,dbs=bts).first()
		if found_user:

			result_net = db.execute("SELECT * FROM {}".format(bts))
			return render_template("view.html", values = result_net)

		else:
			flash("Not Registered..Sign Up first")
			return render_template("home.html")

	return "<h1> Login first </h1>"			


#######################################################################################

# to create database, by enter name and email in website : https://findloc.herokuapp.com
@app.route('/creation', methods=['POST'])
def createdb():
	if request.method == 'POST':
		usr = request.form["usrnm"]
		ema = request.form["emai"]
		namedb = request.form["dbname"]

		a = []
		rand = randint(100,999)
		a.append(rand)
		temp = tmp(usr, ema, namedb, rand)
		mb.session.add(temp)
		mb.session.commit()

		found_user = product.query.filter_by(em=ema,name=usr).first()
		API_KEY = "EG847175400125417698"
		URL = "https://client.myemailverifier.com/clientarea/emailverifier/index.php/verifier/validate_single?email={}&apikey={}".format(ema, API_KEY)
		r = requests.get(url = URL)
		data = r.json()
		status = data['data']['Status']


		if found_user:
			flash("Already Registered ! Login below ")
			return render_template("home.html")

		email_1 = ema.split("@")
		email_2 = email_1[0]
		check = ["{}@gmail.com".format(email_2), "{}@Yahoo.com".format(email_2), "{}@aol.com".format(email_2), "{}@Outlook.com".format(email_2), "{}@iCloud.com".format(email_2), "{}@rediffmail.com".format(email_2)]
		for item in check:
			if ema == item and status == 'Valid':
				try:
					msg = Message("NOTIFICATION FOR HAND WASH !",
						sender="handswash2@gmail.com", # Enter email_id from which you want to send mail to others.
						recipients=[ema])
					msg.body = ""
					msg.html = render_template('ema_vr.html', kaka = a)
					mail.send(msg)

				except Exception as e:
					return str(e)

				return render_template("email_reg.html")

			else:	
				flash("Enter Valid Email !!")
				return render_template("home.html")

	else:
		return render_template("home.html")


################################################################################################        
        

# verify email after signup to create database              
@app.route('/verifyml/<key>')
def veriml(key):
	tepo = tmp.query.filter_by(rand = key).first()

	if tepo:
		nm = tepo.usrnm
		print(nm) 
		em = tepo.ema
		print(em) 
		dbss = tepo.dbs
		dbss = str(dbss)
		print(dbss)

		new_sru = product(nm,em,dbss)
		mb.session.add(new_sru)
		mb.session.commit()
		db.execute("CREATE TABLE IF NOT EXISTS {} (currtime text, currdate text, latitude text, longitude text, accuracy text)".format(dbss))

		mb.session.delete(tepo)
		mb.session.commit()

		return render_template("verifiedea.html")

	else:
		flash("Session Expired !! Sign Up again...")
		return render_template("home.html")


###########################################################
@app.route('/codge', methods= ['POST'])
def codge():
	if request.method == 'POST':
		loti = request.form["loti"]
		lota = request.form["lota"]

		data = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng={}, {}&key=AIzaSyCk1jpJq_k7vj1dfyplU7aLnehWFHlgIe8'.format(loti,lota))
		json_data = data.json()

		chetan = json_data.get('results')	

		print(chetan)

		for i in chetan:
			print(i['formatted_address'])

		return render_template("cogleo.html" , values = chetan)

	else:
		return "<h1> enter details first...</h1>"		


###################################################################
		

	

			













			

