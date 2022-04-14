"""
This script runs the flask_test application using a development server.
"""

from os import environ
from flask_test import app
global PORT
import os
if __name__ == '__main__':
    #HOST = environ.get('SERVER_HOST', 'localhost')
    HOST = '0.0.0.0'
    #PORT = int(environ.get('SERVER_PORT', '8088'))
    PORT = int('8088')
    port_data=open("PORT.txt","w")
    port_data.write(str(PORT))
    port_data.close()

    app.run("0.0.0.0", PORT)
