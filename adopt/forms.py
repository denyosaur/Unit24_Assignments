from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField
from wtforms.validators import InputRequired, NumberRange, URL, Optional

class AddPetForm(FlaskForm):
    '''create a form for all the pet info'''
    name = StringField('Pet Name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat','cat'),('dog','dog'),('porcupine','porcupine'),('bear','bear'),('racoon','racoon'),('deer','deer'),('doge','doge')], validators=[InputRequired()])
    photo_url = StringField('PhotoURL', validators=[Optional(), URL(message="Invalid photo URL")])
    age = IntegerField('Age', validators=[Optional(), NumberRange(0,30, message="Age is not valid")])
    notes = StringField('Notes', [Optional()])
    available = BooleanField('Adoptable')