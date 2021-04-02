from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User,connect_db,db, Feedback
from forms import UserForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY-ECHO"] = True
app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Renders Home page which is the login page """
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_page():
    """Renders registration page during GET and handles
    form data and completes the registration during POST"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data

        new_user = User.register(username,password,email,firstname,lastname)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.error.append('Username is not available. Please choose another username')
            return render_template('register.html',form=form)

        session['username'] = new_user.username
        flash('Your Account Has Been Successfully Created',"success")
        return redirect(f'/users/{username}')
    
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    """Render the login page during GET and handle the login
        form data and authenticate user during POST"""

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!","primary")
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_info_page(username):
    """Once the user is authenticated he is landed on this page."""
    if 'username' not in session:
        flash("Please login first!","danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    form = DeleteForm()
   
    if user.username == session['username']:
       
        return render_template("userinfo.html",user=user,form=form)
    
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Remove the user from the database and also delete all feedbacks associated with the user"""
    if "username" not in session:
        flash("Please login first!","danger")
        return redirect('/login')
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    flash("Deleted User!","info")
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):
    """A form to add feedback during GET and process form data during POST"""
    if "username" not in session:
        flash("Please login first!","danger")
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        title  = form.title.data
        content = form.content.data
        feedback = Feedback(title=title,content=content,username=username)
        db.session.add(feedback)
        db.session.commit()
        flash(f"Feedback added","primary")
        return redirect(f'/users/{feedback.username}')
    return render_template("addfeedback.html",form=form)

@app.route('/feedback/<int:id>/update', methods=["GET","POST"])
def update_feedback(id):
    """Update a feedback during POST and get the update form during GET"""
    feedback = Feedback.query.get_or_404(id)
    if feedback.username != session['username']:
        flash("Please login first!","danger")
        return redirect('/login')
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        flash(f"Edited Feedback Successfully!","info")
        return redirect(f"/users/{feedback.username}")
    return render_template("editfeedback.html",form=form,feedback=feedback)


@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    """Delete Feedback."""

    feedback = Feedback.query.get(id)
    if feedback.username != session['username']:
        flash("Please login first!","danger")
        return redirect('/login')
    
    db.session.delete(feedback)
    db.session.commit()
    flash(f"Feedback deleted","danger")
    return redirect(f"/users/{feedback.username}")

@app.route('/logout')
def logout_page():
    """Logout user and delete session data"""
    session.pop('username')
    flash("Goodbye!","info")
    return redirect('/')