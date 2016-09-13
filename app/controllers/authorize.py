from flask import Blueprint, Flask, flash, render_template, redirect, url_for, session, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_oauthlib.client import OAuth, OAuthException
from app.models.database import db
from app.models.user import User
from app.models.authorize import Authorize
from flask_babel import lazy_gettext

import shortuuid, os
import urllib.request

authorize = Blueprint('authorize', __name__)

oauth = OAuth()

"""Google authenticating https://console.developers.google.com/apis/api"""
google = oauth.remote_app('google',
    consumer_key = 'consumer_key',
    consumer_secret = 'consumer_secret',
    request_token_params = {
        'scope': 'email profile'
    },
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth')

@authorize.route('/oauth2/google')
def google_info():
    callback = url_for('.google_auth', _external = True)
    return google.authorize(callback)

@google.tokengetter
def google_token():
    return session.get('google_token')

@authorize.route('/oauth2/google/callback')
def google_auth():
    resp = google.authorized_response()

    if resp is None:
        flash(lazy_gettext('An error occurred.'), 'danger')
        return redirect('/signin')

    session['google_token'] = (resp['access_token'], '')
    google_user = google.get('userinfo?fields=email,family_name,gender,given_name,hd,id,link,locale,name,picture,verified_email')

    authorize = Authorize.query.\
        filter_by(oauth_id=google_user.data.get('id'), network='google')\
        .first()

    if authorize is None:

        if current_user.is_authenticated():
            user_id = current_user.get_id()

            if not current_user.email or current_user.locale:
                user = User.query.get(user_id)

                if not current_user.email:
                    user.email = google_user.data.get('email')

                if not current_user.locale:
                    user_locale = google_user.data.get('locale')
                    if user_locale:
                        user.locale = user_locale[:2]

                db.session.add(user)
                db.session.commit()

        else:
            user = User(google_user.data.get('name'), None, None)
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            user_locale = google_user.data.get('locale')
            if user_locale:
                user.locale = user_locale[:2]

            user.email = google_user.data.get('email')
            db.session.add(user)
            db.session.commit()

        authorize = Authorize(
            google_user.data.get('id'),
            google_user.data.get('name'),
            google_user.data.get('gender'),
            google_user.data.get('locale'),
            google_user.data.get('verified_email'),
            None,
            google_user.data.get('email'),
            'google',
            user_id)

    else:
        authorize.name = google_user.data.get('name')
        authorize.gender = google_user.data.get('gender')
        authorize.locale = google_user.data.get('locale')
        authorize.verified = google_user.data.get('verified_email')
        authorize.email = google_user.data.get('email')

    db.session.add(authorize)
    db.session.commit()

    if current_user.is_anonymous():
        user = User.query.get(authorize.user_id)
        login_user(user, remember=True)

    return redirect(request.args.get('next') or '/user')

"""Facebook authenticating https://developers.facebook.com/apps"""
facebook = oauth.remote_app('facebook',
    consumer_key = 'consumer_key',
    consumer_secret = 'consumer_secret',
    request_token_params = {
        'scope': 'public_profile, user_friends',
    },
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    access_token_method = 'GET',
    authorize_url = 'https://www.facebook.com/dialog/oauth')

@authorize.route('/oauth2/facebook')
def facebook_info():
    callback = url_for('.facebook_auth', _external = True, next=request.args.get('next') or None)
    return facebook.authorize(callback)

@facebook.tokengetter
def facebook_token():
    return session.get('oauth_token')

@authorize.route('/oauth2/facebook/callback')
def facebook_auth():
    resp = facebook.authorized_response()

    if resp is None or isinstance(resp, OAuthException):
        flash(gettext('An error occurred.'), 'danger')
        return redirect('/signup')

    access_token = resp['access_token']
    session['oauth_token'] = (access_token, '')
    facebook_me = facebook.get('/me?fields=id,name,first_name,last_name,age_range,picture,link,gender,locale,timezone,updated_time,verified')
    facebook_friends = facebook.get('/me/friends')

    authorize = Authorize.query\
        .filter_by(oauth_id=facebook_me.data.get('id'), network='facebook')\
        .first()

    friends = facebook_friends.data.get('summary')
    if friends:
        friends = friends['total_count']

    if authorize is None:

        if current_user.is_authenticated():
            user_id = current_user.get_id()

        else:
            user = User(facebook_me.data.get('name'), None, None)
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            user_locale = facebook_me.data.get('locale')
            if user_locale:
                user.locale = user_locale[:2]
                db.session.add(user)
                db.session.commit()

        authorize = Authorize(
            facebook_me.data.get('id'),
            facebook_me.data.get('name'),
            facebook_me.data.get('gender'),
            facebook_me.data.get('locale'),
            facebook_me.data.get('verified'),
            friends,
            None,
            'facebook',
            user_id)
    else:
        authorize.name = facebook_me.data.get('name')
        authorize.gender = facebook_me.data.get('gender')
        authorize.locale = facebook_me.data.get('locale')
        authorize.verified = facebook_me.data.get('verified')
        authorize.friends = friends

    db.session.add(authorize)
    db.session.commit()

    fb_picture = facebook_me.data.get('picture')
    if fb_picture and authorize.picture != fb_picture['data']['url']:
        try:
            file_name = shortuuid.uuid() + '.jpg'
            file_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(file_folder, file_name)

            url = 'https://graph.facebook.com/{}/picture?type=large&redirect=true&access_token={}'.format(facebook_me.data.get('id'), access_token)
            urllib.request.urlretrieve(url, file_path)

            authorize.picture = fb_picture['data']['url']
            db.session.add(authorize)

            user = User.query.get(authorize.user_id)
            user.picture = file_name
            db.session.add(user)
            db.session.commit()
        except Exception:
            pass

    if current_user.is_anonymous():
        user = User.query.get(authorize.user_id)
        login_user(user, remember=True)

    return redirect(request.args.get('next') or '/user')
