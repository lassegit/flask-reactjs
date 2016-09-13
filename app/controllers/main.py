from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import ContactForm
from app.extensions import cache
from app.models.database import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
# @cache.cached(timeout=300, unless=lambda: current_user.is_authenticated())
def home():
    return render_template('index.html')

@main.route('/about')
# @cache.cached(timeout=300, unless=lambda: current_user.is_authenticated())
def index():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
# @cache.cached(timeout=300, unless=lambda: current_user.is_authenticated())
def contact():
    form = ContactForm()

    if request.method == 'POST' and form.validate_on_submit():
        data = {
            'to' : [current_app.config['CONTACT_MAIL']],
            'from': form.email.data,
            'subject' : 'Support',
            'text': form.message.data
        }
        mailgun.send_email(**data)

        # Remove send form
        form.email.data = None
        form.message.data = None
        form.checksum.data = None

        flash('Thank you. We will get back to you as soon as possible.', 'success')

    return render_template('contact.html', form=form)
