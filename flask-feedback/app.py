from models import User, Feedback, connect_db, db, bcrypt
from forms import RegistrationForm, LoginForm, FeedbackForm
from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
db.create_all()
toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    '''GET route for rendering the registration page
    POST route for registering a new user'''
    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(f'/users/{username}')
    else: 
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''GET route for logging in
    POST route for logging in'''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    """Route for logging out"""
    session.pop("username")
    return redirect("/login")

@app.route('/users/<username>', methods=['GET', 'POST'])
def user_page(username):
    '''route for seeing details of user and making any edits to user info.'''
    if 'username' not in session or username != session['username']:
        return redirect('/login')
    
    user_info = User.query.get(username)
    form = RegistrationForm(obj=user_info)

    if form.validate_on_submit():
        user_info.username = form.username.data
        user_info.email = form.email.data
        user_info.first_name = form.first_name.data
        user_info.last_name = form.last_name.data
        db.session.add(user_info)
        db.session.commit()
        return redirect('/users/<username>')

    return render_template('user_info.html', form=form, user=user_info)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''post route for deleting user'''
    if 'username' not in session or username != session['username']:
        return redirect('/login')

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    session.pop('username')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''GET route for page to add feedback.
    POST route for adding feedback to DB'''
    if 'username' not in session or username != session['username']:
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect('/users/<username>')
        
    return render_template('add_feedback.html', form=form, username=username)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''app route for updating feedback'''
    if 'username' not in session:
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    return render_template('add_feedback.html', form=form, username=feedback.username)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''app route for deleting feedback''' 
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit() 

    return redirect(f'/users/{feedback.username}')
    
