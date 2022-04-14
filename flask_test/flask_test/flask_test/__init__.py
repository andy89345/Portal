"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)
app.config.update({

'TEMPLATES_AUTO_RELOAD':True
})
#app.config["TEMPLATES_AUTO_RELOAD"] = True

import flask_test.views
