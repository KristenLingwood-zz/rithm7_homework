import psycopg2
from flask import Flask, render_template, redirect, request, url_for
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
modus = Modus(app)
toolbar = DebugToolbarExtension(app)

DB = "postgresql://localhost/userzap"

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text)
    messages = db.relationship('Message', backref='user')


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


db.create_all()


@app.route('/')
def root():
    return "Usersapp...user zap... get it?"


@app.route('/users')
def users_index():
    """show all users"""
    users = User.query.all()
    return render_template("users/index.html", users=users)


@app.route('/users/new')
def users_new():
    """show create user form"""
    return render_template('users/new.html')


@app.route('/users', methods=["POST"])
def users_create():
    """create new user from form and add to db"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        img_url=request.form['img_url'])
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('users_index'))


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """show individual user's page"""
    found_user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=found_user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """show edit form"""
    found_user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=found_user)


@app.route('/users/<int:user_id>', methods=['PATCH'])
def users_update(user_id):
    """update user info and return to user show page"""
    found_user = User.query.get(user_id)
    found_user.first_name = request.form['first_name'],
    found_user.last_name = request.form['last_name'],
    found_user.img_url = request.form['img_url']
    db.session.add(found_user)
    db.session.commit()
    return redirect(url_for('users_index'))


@app.route('/users/<int:user_id>', methods=['DELETE'])
def users_destroy(user_id):
    """delete user"""
    found_user = User.query.get(user_id)
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for("users_index"))


@app.route('/users/<int:user_id>/messages')
def messages_index(user_id):
    """show all messages for user"""
    found_user = User.query.get(user_id)
    return render_template('messages/show.html', user=found_user)


@app.route('/users/<int:user_id>/messages/new')
def messages_new(user_id):
    """show new message form"""
    found_user = User.query.get(user_id)
    return render_template('messages/new.html', user=found_user)


@app.route('/users/<int:user_id>/messages', methods=['POST'])
def messages_create(user_id):
    """create new message and add to db"""
    found_user = User.query.get(user_id)
    content = request.form['message_content']
    new_message = Message(content)
    db.session.add(new_message)
    db.commit()
    return redirect(url_for('messages_index', user=found_user))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404