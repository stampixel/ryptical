# routes
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user # if the user is logged in, current_user will give us information on the user, such as name, password, links
from .models import Link, User
from . import db
import validators

views = Blueprint('views', __name__)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        url = request.form['url']
        display_url = request.form['display_url']

        valid=validators.url(url)
        print(valid)

        if len(url) < 1 or len(display_url) < 1:
            flash("Values can't be blank!", category='error')
        if valid != True:
            print("invalid")
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


    return render_template("editor.html", user=current_user) # we will be able to do stuff

@views.route('/')
def index():
    return render_template('index.html', user=current_user)

@views.route('/@<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

