from flask import request, jsonify, current_app

# Example helper function
def json_error(message='An error happend', status_code = 500):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response
    
# http://flask.pocoo.org/snippets/33/
def timeago(dt):
    if not dt:
        return ''

    now = datetime.utcnow()
    diff = abs(now - dt)

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s ago" % (period, singular if period == 1 else plural)

