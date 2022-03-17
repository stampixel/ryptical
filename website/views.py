# routes
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user # if the user is logged in, current_user will give us information on the user, such as name, password, links
from .models import Link, User, Profile
from . import db
import validators

views = Blueprint('views', __name__)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':

        # make a seperate route for this, do what you did for /delete/
        try:
            if request.form['update_profile'] == 'Update Profile':
                print("hello world")
                pfp = request.form['pfp']
                background = request.form['background']
                pfp_valid = validators.url(pfp)
                background_valid = validators.url(background)

                # delete_profile = Profile.query.get(user_id=current_user.id)
                delete_profile = Profile.query.filter_by(user_id=current_user.id).first()

                if pfp == '':
                    pfp = delete_profile.pfp
                if background == '':
                    background = delete_profile.background

                try:
                    try:
                        db.session.delete(delete_profile)
                        db.session.commit()
                    except:
                        pass

                    # GET THAT CHECKED, THE PROFILE ISNT BEING ADDED TO THE DATABASE FOR SOME REASON
                    new_profile = Profile(pfp=pfp, background=background, user_id=current_user.id)
                    db.session.add(new_profile)
                    db.session.commit()

                    new_profile = Profile.query.filter_by(user_id=current_user.id).first()
                    flash('Successfully saved new PFP and/or wallpaper!', category='success')
                    return render_template('editor.html', user=current_user)
                except:
                    flash('Something went wrong, try again later!', category='error')

        except:
            pass

        try:
            if request.form['add_link'] == 'Add Link':
                url = request.form['url']
                display_url = request.form['display_url']

                valid = validators.url(url)
                print(valid)

                if len(url) < 1 or len(display_url) < 1:
                    flash("Values can't be blank!", category='error')
                if valid != True:
                    url = f"https://{url}"
                    valid = validators.url(url)
                    if valid == True:
                        new_link = Link(url=url, display_url=display_url, user_id=current_user.id)
                        db.session.add(new_link)
                        db.session.commit()
                        flash('Link added!', category='success')
                    else:
                        flash('URL needs to be valid, example: https://tankated.ga', category='error')
                else:
                    new_link = Link(url=url, display_url=display_url, user_id=current_user.id)
                    db.session.add(new_link)
                    db.session.commit()
                    flash('Link added!', category='success')
        except:
            pass

    return render_template("editor.html", user=current_user) # we will be able to do stuff

@views.route('/')
def index():
    return render_template('index.html', user=current_user)

@views.route('/@<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

