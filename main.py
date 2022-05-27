from api import create_app
from flask import jsonify
import pyodbc

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)