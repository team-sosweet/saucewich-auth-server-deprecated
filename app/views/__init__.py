from sanic import Sanic

from app.views import login, logout, register


def register_blueprints(app: Sanic):
    app.blueprint(login.blueprint)
    app.blueprint(logout.blueprint)
    app.blueprint(register.blueprint)
