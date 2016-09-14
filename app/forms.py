from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, RadioField
from wtforms import validators
from flask_login import current_user
from flask_babel import lazy_gettext
from werkzeug.security import check_password_hash

from app.models.database import db
from app.models.user import User

class SignupForm(Form):
    email = TextField(u'email', validators=[validators.required(), validators.Email()])
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])

    def validate(self):
        check_validate = super(SignupForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email is already taken.")
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username is already taken.")
            return False

        return True

class LoginForm(Form):
    email = TextField(u'email', validators=[validators.required()])
    # username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("Invalid email or password")
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.email.errors.append("Invalid email or password")
            return False

        return True

class UserForm(Form):
    username = TextField(u'Username', validators=[validators.required()])
    email = TextField(u'email', validators=[validators.required()])
    phone = TextField(u'Phone', validators=[validators.required()])
    body = TextAreaField(u'Body', validators=[])

    def validate(self):
        check_validate = super(UserForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter(User.id != current_user.get_id(), User.email == self.email.data).first()
        if user:
            self.email.errors.append('Email is already taken.')
            return False

        return True

class ContactForm(Form):
    email = TextField(u'email', validators=[validators.required(), validators.Email()])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    checksum = TextField(u'human', validators=[])

    def validate(self):
        check_validate = super(ContactForm, self).validate()

        if not check_validate:
            return False

        if current_user.is_anonymous() and self.checksum.data != '4':
            self.checksum.errors.append('The answer is: 4')
            return False

        return True

class PasswordForm(Form):
    old_password = PasswordField(u'Old password', validators=[])
    new_password = PasswordField(u'New password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField(u'New password', validators=[validators.DataRequired()])

    def validate(self):
        check_validate = super(PasswordForm, self).validate()

        if not check_validate:
            return False

        if current_user.password and not check_password_hash(current_user.password, self.old_password.data):
            self.old_password.errors.append(lazy_gettext('Old password not correct.'))
            return False

        return True

