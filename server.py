from flask import Flask


def startServer():
    from views import views

    app = Flask(__name__)
    app.register_blueprint(views, url_prefix="/")

    app.run(debug=False, port=42069)
