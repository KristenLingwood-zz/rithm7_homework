from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Optional, URL, NumberRange
import requests
import os
import websiteconfig

PLACEHOLDER_IMG = "https://image.freepik.com/free-vector/unicorn-background-design_1324-79.jpg"

app = Flask(__name__)

app.debug = websiteconfig.DEBUG
app.config['SECRET_KEY'] = "abc123"
app.pf_api_key = websiteconfig.pf_api_key
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

    def image_url(self):
        """return the pet image or a placeholder"""
        # self references instance of class
        return self.photo_url or PLACEHOLDER_IMG


db.create_all()


class AddPetForm(FlaskForm):
    """form for adding pets"""
    name = StringField("pet name", validators=[InputRequired()])
    species = RadioField(
        "Species",
        choices=[('cat', 'Cat'), ('dog', 'Dog'), ('dragon', 'Dragon')])
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
    photo_url = StringField(
        "url", validators=[Optional(), URL(message="bad url")])
    notes = TextAreaField("notes", validators=[Optional()])
    available = BooleanField("Available?")


def get_random_petfinder_pet():
    """get random pet from petfinder and return dict of info"""
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
    # if info['media']['photos']['photo']:
    #     photo_url = info['media']['photos']['photo'][1].get('$t')
    # else: 
    #     photo_url = generic image

    return render_template('index.html', pets=pets, pf_pet_info=pf_pet_info)


@app.route('/add', methods=['GET', 'POST'])
def pets_add():
    """add new pet form and handler"""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash("pet added!")
        return redirect(url_for('pets_index'))

    else:
        return render_template('add.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pets_edit(pet_id):
    """update pet info"""

    found_pet = Pet.query.get_or_404(pet_id)

    form = AddPetEditForm(obj=found_pet)

    if form.validate_on_submit():
        found_pet.notes = form.data['notes']
        found_pet.photo_url = form.data['photo_url']
        found_pet.available = form.data['available']
        db.session.commit()
        flash(f"{found_pet.name} updated.")
        return redirect(url_for('pets_index'))

    else:
        return render_template('edit.html', form=form, found_pet=found_pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """return json string for given pet in db"""
    pet = Pet.query.get_or_404(pet_id)
    info = {
        "name": pet.name,
        "age": pet.age,
        "photo": pet.photo_url,
        "notes": pet.notes,
        "available": pet.available
    }

    return jsonify(info)