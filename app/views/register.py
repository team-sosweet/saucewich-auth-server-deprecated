from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.models.account import Account

blueprint = Blueprint('register-api', url_prefix='/register')


class RegisterView(HTTPMethodView):
    async def post(self, request: Request):
        try:
            username: str = request.json['username']
            password: str = request.json['password']
            nickname: str = request.json['nickname']
        except KeyError:
            abort(400)

        return json({
            'success': await Account.register(username, password, nickname)
        })


blueprint.add_route(RegisterView.as_view(), '/')
