from flask import Flask, Blueprint, request, current_app, json
import jinja2, os
import app.helper as helper

tpl_filter = Blueprint('tpl_filter', __name__)

@tpl_filter.app_template_filter('timeago')
def timeago(date):
    return helper.timeago(date)

@tpl_filter.app_template_filter('get_assets')
def get_assets(asset_type):
    path = os.path.join(current_app.root_path, current_app.config['TEMPLATE_FOLDER'], 'assets.json')
    assets = json.load(open(path, 'r'))
    output = ''

    if asset_type == 'css':
        output = '<link rel="stylesheet" href="{0}">'.format(assets['style']['css'])

    elif asset_type == 'js':
        manifest = assets['manifest']['js']
        manifest = manifest[1:]

        manifest_file = open(os.path.join(current_app.root_path, current_app.config['STATIC_FOLDER'], manifest), 'r')
        output += '<script>' + manifest_file.read() + '</script>'
        manifest_file.close()

        output += '<script src="{0}"></script>'.format(assets['vendor']['js'])
        output += '<script src="{0}"></script>'.format(assets['app']['js'])

    return jinja2.Markup(output)
