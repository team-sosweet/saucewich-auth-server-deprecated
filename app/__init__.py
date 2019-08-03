from sanic import Sanic

from app.misc.listener import register_listeners
from app.views import register_blueprints


def create_app() -> Sanic:
    app = Sanic(__name__)

    register_blueprints(app)
    register_listeners(app)

    return app
