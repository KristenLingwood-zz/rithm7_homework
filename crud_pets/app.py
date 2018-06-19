import psycopg2
from flask import Flask, render_template, redirect, request, url_for
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
modus = Modus(app)
toolbar = DebugToolbarExtension(app)

DB = "postgresql://localhost/crud_pets"

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Pets(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    species = db.Column(db.Text)
    breed = db.Column(db.Text)
    human = db.Column(db.Text)


db.create_all()
# count = 1

# def __init__(self, name, species, breed, human):
#     self.name = name
#     self.species = species
#     self.breed = breed
#     self.human = human
#     self.id = Pets.count
#     Pets.count += 1

# finn = Pets("Mister Finnigan", "cat", "tabby", "Clara")
# sadie = Pets("Sadie", "dog", "cattle dog", "Allie")
# cali = Pets("Cali", "cat", "calico", "Toni")
# whiskey = Pets("Whiskey", "dog", "office", "Matt")
# norbert = Pets("Norbert", "dragon", "Norwegian Ridgeback", "Hagrid")

# pets = [finn, sadie, cali, whiskey, norbert]


# root
@app.route('/')
def root():
    return "Is it Caturday yet?"


# landing/show all page
@app.route('/pets', methods=['GET'])
def index():
    """show list of all pets"""
    pets = Pets.query.all()
    return render_template('index.html', pets=pets)


# create new
@app.route('/pets/new', methods=['GET'])
def new():
    return render_template('new.html')


# handle new form and display updated list
@app.route('/pets', methods=['POST'])
def create():
    """create new instance of Pets class and add to db"""
    new_pet = Pets(
        name=request.form['name'],
        species=request.form['species'],
        breed=request.form['breed'],
        human=request.form['human'])
    db.session.add(new_pet)
    db.session.commit()
    return redirect(url_for('index'))


# get info on individual pet
@app.route('/pets/<int:id>', methods=['GET'])
def show(id):
    pet = Pets.query.get_or_404(id)
    # pet = Pets.query.filter(Pets.id == id).one()
    # found_pet = [pet for pet in pets if pet.id == id][0]
    return render_template("show.html", pet=pet)


@app.route('/pets/<int:id>', methods=['DELETE'])
def destroy(id):
    pet = Pets.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/pets/<int:id>/edit', methods=['GET'])
def edit(id):
    pet = Pets.query.get_or_404(id)
    return render_template('edit.html', pet=pet)


@app.route('/pets/<int:id>', methods=['PATCH'])
def update(id):
    name = request.form['name'],
    species = request.form['species'],
    breed = request.form['breed'],
    human = request.form['human']
    pet = Pets.query.get_or_404(id)
    pet.name = name
    pet.species = species
    pet.breed = breed
    pet.human = human
    db.session.commit()

    return redirect(url_for('show', id=pet.id))


# need to figure out how to catch when ID given is not found
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
