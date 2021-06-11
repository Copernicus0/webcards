

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class FForm(FlaskForm):
	firstname=StringField('First Name',validators=[DataRequired(),Length(min=2, max= 30)])
	lastname=StringField('Last Name',validators=[DataRequired(),Length(min=2, max= 30)])
	email=StringField('Email',validators=[DataRequired(),Length(min=2, max= 30)])
	submit=SubmitField('Submit')