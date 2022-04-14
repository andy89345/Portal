"""
This script runs the ajax_data application using a development server.
"""

from os import environ
from ajax_data import app

if __name__ == '__main__':
    HOST = "0.0.0.0"
   
    PORT = int('8087')
    
    app.run("0.0.0.0", PORT)
