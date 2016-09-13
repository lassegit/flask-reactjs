from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import cache
from app.forms import LoginForm, SignupForm
from app.models.database import db
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated():
        return redirect('/user')

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        return redirect(request.args.get('next') or '/user')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated():
        return redirect('/user')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()

        login_user(user, remember=True)

        return redirect(request.args.get('next') or '/user')

    return render_template('signin.html', form=form)


@auth.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('facebook_token', None)

    logout_user()

    flash('You have been logged out.', 'success')

    return redirect('/signin')
