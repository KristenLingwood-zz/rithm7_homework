from flask import Flask, render_template, redirect, request, url_for, session
from flask_modus import Modus
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
modus = Modus(app)
toolbar = DebugToolbarExtension(app)

DB = "postgresql://localhost/userzap"

app.config['SQLALCHEMY_DATABASE_URI'] = DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text)
    messages = db.relationship(
        'Message', backref='user', lazy="dynamic", cascade="all,delete")

    @classmethod
    def register(cls, username, password):
        """register a user and hash their password"""
        # take password and generate a bcrypt hash, saved to var hashed
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """valid if user exists and password is correct"""
        user = User.query.filter_by(username=username).first()
        # if user exists
        if user:
            # if password is correct
            if bcrypt.check_password_hash(user.password, password):
                return user

        return False


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


message_tags = db.Table(
    'message_tags',
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, unique=True)
    messages = db.relationship(
        'Message',
        lazy="dynamic",
        secondary=message_tags,
        cascade="all,delete",
        backref=db.backref('tags', lazy="dynamic"))


db.create_all()


@app.route('/')
def root():
    return redirect(url_for('users_index'))


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
    username = request.form.get("username")
    password = request.form.get("password")
    new_user = User.register(username=username, password=password)
    fname = request.form['first_name']
    lname = request.form['last_name']
    img = request.form['img_url']
    if fname == "":
        raise ValueError('First name must not be blank')
    if lname == "":
        raise ValueError('Last name must not be blank')
    new_user.first_name = fname
    new_user.last_name = lname,
    new_user.img_url = img,
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('users_index'))


@app.route('/login', methods=['GET', 'POST'])
def users_login():
    """handle log in form. Authenticate and redirect to secret welcome page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logged_in_user = User.authenticate(username, password)
        if logged_in_user:
            session['user_id'] = logged_in_user.id
            return redirect(url_for('users_welcome', user=logged_in_user))

    return render_template('/users/login.html')


@app.route('/users/welcome')
def users_welcome():
    """show welcome form for logged in user"""
    if session['user_id']:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('users/welcome.html', user=user)


@app.route('/users/logout')
def users_logout():
    """Logout a user"""
    if session['user_id']:
        del session['user_id']
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
    found_user = User.query.get_or_404(user_id)
    found_user.first_name = request.form['first_name'],
    found_user.last_name = request.form['last_name'],
    found_user.img_url = request.form['img_url']
    db.session.add(found_user)
    db.session.commit()
    return redirect(url_for('users_show', user_id=found_user.id))


@app.route('/users/<int:user_id>', methods=['DELETE'])
def users_destroy(user_id):
    """delete user"""
    found_user = User.query.get_or_404(user_id)
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for("users_index"))


@app.route('/users/<int:user_id>/messages')
def messages_index(user_id):
    """show all messages for user"""
    found_user = User.query.get_or_404(user_id)
    return render_template('messages/index.html', user=found_user)


@app.route('/users/<int:user_id>/messages/new')
def messages_new(user_id):
    """show new message form"""
    found_user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('messages/new.html', user=found_user, tags=tags)


@app.route('/users/<int:user_id>/messages', methods=['POST'])
def messages_create(user_id):
    """create new message and add to db"""
    content = request.form['message_content']
    new_message = Message(content=content, user_id=user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    new_message.tags = Tag.query.filter(Tag.id.in_(tag_ids))
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('messages_index', user_id=user_id))


@app.route('/messages/<int:message_id>')
def messages_show(message_id):
    """show specific message"""

    found_message = Message.query.get_or_404(message_id)
    return render_template('/messages/show.html', message=found_message)


@app.route('/messages/<int:message_id>', methods=['DELETE'])
def messages_destroy(message_id):
    """delete a message"""
    found_message = Message.query.get_or_404(message_id)
    user = found_message.user
    db.session.delete(found_message)
    db.session.commit()
    return redirect(url_for('messages_index', user_id=user.id))


@app.route('/messages/<int:message_id>/edit')
def messages_editform(message_id):
    found_message = Message.query.get_or_404(message_id)
    tags = Tag.query.all()
    return render_template(
        'messages/edit.html', message=found_message, tags=tags)


@app.route('/messages/<int:message_id>', methods=['PATCH'])
def messages_update(message_id):
    """hand messages_editform and update message info"""
    found_message = Message.query.get_or_404(message_id)
    found_message.content = request.form['message_content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    found_message.tags = Tag.query.filter(Tag.id.in_(tag_ids))
    user = found_message.user
    db.session.add(found_message)
    db.session.commit()
    return redirect(url_for('messages_index', user_id=user.id))


@app.route('/tags')
def tags_index():
    """Show all tags"""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new():
    """show new tag form"""
    messages = Message.query.all()
    return render_template('tags/new.html', messages=messages)


@app.route('/tags', methods=['POST'])
def tags_create():
    """handle new tag form"""
    content = request.form.get('tag_content')
    new_tag = Tag(content=content)
    message_ids = [int(num) for num in request.form.getlist("messages")]
    new_tag.messages = Message.query.filter(Message.id.in_(message_ids))
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('tags_index'))


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """show individual tag"""
    found_tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=found_tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_editform(tag_id):
    """show edit form"""
    found_tag = Tag.query.get_or_404(tag_id)
    messages = Message.query.all()
    return render_template('tags/edit.html', tag=found_tag, messages=messages)


@app.route('/tags/<int:tag_id>', methods=['PATCH'])
def tags_update(tag_id):
    """update tag info and return to tag show page"""
    found_tag = Tag.query.get_or_404(tag_id)
    found_tag.content = request.form['tag_content']
    message_ids = [int(num) for num in request.form.getlist("messages")]
    found_tag.messages = Message.query.filter(Message.id.in_(message_ids))
    db.session.add(found_tag)
    db.session.commit()
    return redirect(url_for('tags_index'))


@app.route('/tags<int:tag_id>', methods=['DELETE'])
def tags_destroy(tag_id):
    """delete tag"""
    found_tag = Tag.query.get_or_404(tag_id)
    db.session.delete(found_tag)
    db.session.commit()
    return redirect(url_for('tags_index'))


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404
