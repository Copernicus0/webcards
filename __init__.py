from flask import Flask,render_template,request,redirect,url_for,session
#for form
from form.form import FForm

#for filename of img
from werkzeug.utils import secure_filename
import os

from PIL import Image, ImageFont, ImageDraw 


app = Flask(__name__)

#to put in dotenv???
app.config['SECRET_KEY']='okboomer'



@app.route("/")
def home():
	return "hello world"

#set upload folder for image
app.config["IMAGE_UPLOADS"] = "/upload"
#allowed extensions for img
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
#max size
app.config["MAX_IMAGE_FILESIZE"] = 1024*1024*1024

#verify if img has . in it
def allowed_image(filename):
	if not "." in filename:
		return False
#verify if extension is valid
	ext = filename.rsplit(".", 1)[1]

	# #
	# session['img_ext']=ext


	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False
#verify if file size is allowed 
def allowed_image_filesize(filesize):
	if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
		return True
	else:
		return False

#form to complete
@app.route("/form", methods=["GET", "POST"])
def form():
	#form it's equal to the class form defined in form.py
	form=FForm()
	#check if method is post
	if request.method == "POST":

		if request.files:
			print(request.cookies)

			if "filesize" in request.cookies:
				if not allowed_image_filesize(request.cookies["filesize"]):
					print("Filesize exceeded maximum limit")
					return redirect(request.url)
				#image it's equal to image name from form.html
				image = request.files["image"]

				
				

				#check if filename is empty
				if image.filename == "":
					print("No filename")
					return redirect(request.url)

				#check if image is allowed
				if allowed_image(image.filename):

					filename = secure_filename(image.filename)

					#gets color from imput name="color_pick"
					color_pick=request.values.get("color_pick")

					phone=request.values.get("phone")

					occupation=request.values.get("occupation")


					ext=filename.rsplit('.',1)[1]
					img_upload="upload."+ext



					#image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

					#save image in upload folder
					image.save(os.path.join(".","images","upload",img_upload))
					print("Image saved")

					#save variables and transmit them throught the session
					session['filename'] = img_upload
					session['firstname']=form.firstname.data
					session['lastname']=form.lastname.data
					session['email']=form.email.data
					session['color_pick']=color_pick
					session['phone']=phone
					session['occupation']=occupation


					#return redirect(url_for("edit",filename=filename))

					#redirect to edit function
					return redirect(url_for("edit"))
				else:
					#redirect to request.url = redirect to the page that made the request = /form
					print("That file extension is not allowed")
					return redirect(request.url)
	return render_template("form.html",form=form)



@app.route("/edit")
def edit():
	#filename = request.args['filename']

	#get variables from session
	filename = session['filename'] 
	first_name=session['firstname']
	last_name=session['lastname']
	email=session['email']
	color=session['color_pick']
	phone=session['phone']
	occupation=session['occupation']

	#print(filename+" "+first_name+" "+last_name)



	
	#get image from folder
	my_image = Image.open(os.path.join(".","images","upload",filename))
	width, height = my_image.size
	#get font from folder
	title_font = ImageFont.truetype(os.path.join(".",'OpenSans-Regular.ttf'), 80)
	
	#create an image duplicate that is's editable
	image_editable = ImageDraw.Draw(my_image)
	#put the text on the image
	image_editable.text(((width/2)-0.3*width,(height/2)-0.3*height),"First Name: "+ first_name, color, font=title_font)
	image_editable.text(((width/2)-0.3*width,(height/2)-0.2*height),"Last Name: "+ last_name, color, font=title_font)
	image_editable.text(((width/2)-0.3*width,(height/2)-0.1*height),"Email: "+ email, color, font=title_font)
	image_editable.text(((width/2)-0.3*width,(height/2)-0*height),"Phone: "+ phone, color, font=title_font)
	image_editable.text(((width/2)-0.3*width,(height/2)+0.1*height),"Occupation: "+ occupation, color, font=title_font)
	
	#save the image

	ext=filename.rsplit('.',1)[1]
	out="result."+ext

	my_image.save(os.path.join(".","images","result",out))
	print(str(width)+" "+str(height))
	
	return "nice"
	#return render_template("img.html")

if __name__== "__main__":
	app.run(debug=True)
