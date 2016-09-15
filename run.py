#!/usr/bin/env python
import os

from app import create_app

env = os.environ.get('app_ENV', 'prod')
app = create_app('app.settings.%sConfig' % env.capitalize(), env=env)

if __name__ == '__main__':
    app.run()
