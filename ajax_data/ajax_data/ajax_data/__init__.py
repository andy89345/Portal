"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import ajax_data.views
app.config.update({
'DEBUG':True,
'TEMPLATES_AUTO_RELOAD':True
})