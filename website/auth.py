from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User, Link, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # imports it from the __init__ file
from flask_login import login_user, login_required, logout_user, current_user
# hasing makes the encrypted thing irriversible

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first() # filtering all the user that have that specific username
        if user: # checks password
            if check_password_hash(user.password, password): # checks if the password inside the db equals to the hashed(password) that the user entered
                flash('Logged in successfully!', category='success')
                login_user(user = User.query.filter_by(username=username).first(), remember=True)
                
                
                return redirect(url_for('views.home'))
           
            else:
                flash('Incorrect password, try again. (contact stampixel to reset it).', category='error')
        else:
            flash("Username does nto exist, try registering an account!", category='error')



    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #only allows accesss to this route if the user is already logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists, try again!", category='error')
        elif password1 != password2:
            flash("Paswords must match!", category='error')
        elif len(username) > 24:
            flash("Username must be less than 24 characters!", category='error')
        elif len(username) < 2:
            flash("Username to short!", category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256')) # learn about sha256
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(username=username).first()   
            assert user.is_active
            login_user(user, remember=True)  

            defualt_profile = Profile(pfp='https://i.imgur.com/eNsgEu8.png', background="https://i.imgur.com/CgGv8p8.png", user_id=current_user.id)
            db.session.add(defualt_profile)
            db.session.commit()          

            flash("Successfully created account!", category='success')
            
            
            return redirect(url_for('views.home')) # views is the blueprint, home is the function. We could also just do "/"

    return render_template("register.html", user=current_user)

@auth.route('/delete/<int:id>')
@login_required
def delete_link(id):
    link_to_delete = Link.query.get_or_404(id)
    try:
        db.session.delete(link_to_delete)
        db.session.commit()
        return redirect(url_for('views.home'))
    except:
        flash('Try again later.', category='error')



@auth.route('/edit/<int:id>') # remember to edit editor.html to make the thing redirect to here
@login_required
def edit_link(id):
    pass

# @auth.route('/admin', methods=['GET', 'POST'])
# def admin_panel():
#     print("hello world")
#     if request.method == 'POST':
#         password = generate_password_hash(request.form['password'], method='sha256')
#         print(password)
#         if check_password_hash("sha256$WWssn1fvjk0J4HLU$eb14659a7bca91d2b6b4f5a2093da7a274c9b7fa036fcdc033c68d2a5ec3350a", password):
#             print("hellowrodl")
#             return render_template("admin_panel.html")
#     return render_template("admin.html") # make html for admin panel.
