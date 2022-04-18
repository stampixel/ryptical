# routes
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from .models import Link, User, Profile
from . import db
from flask_admin.contrib.sqla import ModelView

admin = Blueprint('admin', __name__)



# admin.add_view(ModelView(User, db.session))

