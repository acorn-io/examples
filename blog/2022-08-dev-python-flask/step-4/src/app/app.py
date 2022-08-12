from flask import Flask

from app.web import bp as web

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

app.register_blueprint(web)
