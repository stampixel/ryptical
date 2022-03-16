# routes
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user # if the user is logged in, current_user will give us information on the user, such as name, password, links
from .models import Link
from . import db

views = Blueprint('views', __name__)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        url = request.form['url']
        display_url = request.form['display_url']

        if len(url) < 1 or len(display_url) < 1:
            flash("Values can't be blank!", category='error')
        else:
            new_link = Link(url=url, display_url=display_url, user_id=current_user.id)
            db.session.add(new_link)
            db.session.commit()
            flash('Link added!', category='success')
    return render_template("editor.html", user=current_user) # we will be able to do stuff

@views.route('/')
def index():
    return render_template('index.html', user=current_user)

