from flask_wtf import FlaskForm
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import Pet, connect_db, db
from forms import AddPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    '''homepage for the app. shows list of all available pets and the option to add a new pet'''
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    '''app route to adding of new pet to SQL db.'''
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        new_pet = Pet(name=name, species=species, photo_url=photo, age=age, notes=notes, available=available)

        db.session.add(new_pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add-pet.html', form=form)
    
@app.route('/<int:pet_id>', methods=['GET','POST'])
def display_pet_info(pet_id):
    '''app route that shows pet info and allows for editing.
    any changes will be made in SQL db as well.'''
    pet_info = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet_info)
    if form.validate_on_submit():
        pet_info.name = form.name.data
        pet_info.species = form.species.data  
        pet_info.photo_url = form.photo_url.data
        pet_info.age = form.age.data
        pet_info.notes = form.notes.data

        db.session.add(pet_info)
        db.session.commit()
        return redirect(f'/{pet_id}')
    else:
        return render_template('pet-info.html', form=form)
