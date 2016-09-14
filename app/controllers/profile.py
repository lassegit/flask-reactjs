from flask import Blueprint, render_template, flash, request, redirect, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.extensions import cache
from app.forms import UserForm, PasswordForm
from app.models.database import db
from app.models.user import User
from app.models.authorize import Authorize
import app.helper as helper

profile = Blueprint('profile', __name__)

@profile.route('/user')
@login_required
def user():
    user = User.query.get(current_user.get_id())
    return render_template('user.html', user=user)

@profile.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.query.get(current_user.get_id())

    form = UserForm()
    if form.username.data is None:
        form.username.data = user.username
    if form.email.data is None:
        form.email.data = user.email
    if form.phone.data is None:
        form.phone.data = user.phone

    if form.validate_on_submit():
        user = db.session.query(User).get(current_user.get_id())
        user.username = form.username.data
        user.email = form.email.data

        if form.phone.data:
            user.phone = form.phone.data.replace(' ', '')
        else:
            user.phone = None

        db.session.add(user)
        db.session.commit()

        return redirect(request.args.get('next') or '/user')

    return render_template('user_edit.html', form=form, user=user)


@profile.route('/user/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.query.get(current_user.get_id())
    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.get_id())
        user.password = generate_password_hash(form.new_password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your password have been updated.', 'success')
        return redirect(request.args.get('next') or '/user')

    return render_template('user_password.html', user=user, form=form)
