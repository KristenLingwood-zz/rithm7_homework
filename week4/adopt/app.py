import sys
print(sys.path)

import psycopg2
from flask import Flask, render_template, redirect, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
pf_api_key = os.environ['PF_API_KEY']
toolbar = DebugToolbarExtension(app)

DB = "postgresql://localhost/adopt"

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)


class AddPetForm(FlaskForm):
    """form for adding pets"""
    name = StringField("pet name", validators=[InputRequired()])
    #    could do radio field species =RadioField("Species", choices=[])
    species = StringField(
        "species",
        validators=[
            InputRequired(),
            AnyOf(
                ['cat', 'dog', 'dragon'],
                message="please pick a cat, dog, or dragon")
        ])
    photo_url = StringField("url", validators=[Optional(), URL()])
    age = FloatField(
        "age",
        validators=[
            InputRequired(),
            NumberRange(min=0, max=30, message='Age must be 0-30')
        ])
    notes = StringField("notes")


class AddPetEditForm(FlaskForm):
    """form for updating pet info"""
    photo_url = StringField("url", validators=[Optional(), URL()])
    notes = StringField("notes")
    available = BooleanField("Available", validators=[InputRequired()])


db.create_all()


def get_random_petfinder_pet():
    r = requests.get("http://api.petfinder.com/pet.getRandom", {
        "key": pf_api_key,
        "format": "json",
        "output": "basic"
    })
    return r.json()['petfinder']['pet']


@app.route('/')
def pets_index():
    """landing page, show all pets"""
    pets = Pet.query.all()

    pf_pet = get_random_petfinder_pet()

    pf_pet_info = {
        "name": pf_pet['name'].get('$t'),
        'age': pf_pet.get('age').get('$t'),
        'photo': pf_pet['media']['photos']['photo'][1].get('$t'),
        'description': pf_pet.get('description').get('$t')
    }

    return render_template('index.html', pets=pets, pf_pet_info=pf_pet_info)


@app.route('/add', methods=['GET', 'POST'])
def pets_add():
    """add new pet form and handler"""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.data['name']
        species = form.data['species']
        photo_url = form.data['photo_url']
        age = form.data['age']
        notes = form.data['notes']

        # data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        # new_pet = Pet(**data)
        new_Pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes)
        db.session.add(new_Pet)
        db.session.commit()
        # flash("pet added!")
        return redirect(url_for('pets_index'))

    else:
        return render_template('add.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pets_show(pet_id):
    """show info for individual pet"""
    found_pet = Pet.query.get(pet_id)
    return render_template('show.html', pet=found_pet)


@app.route('/<int:pet_id>/edit', methods=['GET', 'PATCH', 'DELETE'])
def pets_edit(pet_id):
    """update pet info"""

    found_pet = Pet.query.get_or_404(pet_id)

    form = AddPetEditForm(obj=found_pet)

    if form.validate_on_submit():
        found_pet.photo_url = form.data['photo_url']
        found_pet.age = form.data['age']
        found_pet.notes = form.data['notes']
        db.session.commit()
        # flash(f"{found_pet.name} updated.") need to import flash
        return redirect(url_for('pets_show', pet_id=pet_id, form=form))

    else:
        return render_template('edit.html', form=form, found_pet=found_pet)


# @app.route("/api/pets/<int:id>", methods=['GET'])
# def api_get_pet(pet_id):
#     pet = Pet.query.get_or_404(pet_id)
#     info = {"name": pet.name, "age"=pet.age, "photo"=}
