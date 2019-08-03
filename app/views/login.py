from uuid import uuid4

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from werkzeug.security import check_password_hash

from app.models.account import Account
from app.models.session import Session

blueprint = Blueprint('login-api', url_prefix='/login')

class LoginView(HTTPMethodView):
    async def post(self, request: Request):
        username: str = request.json['username']
        password: str = request.json['password']

        account = await Account.get(username)

        if account is None:
            abort(404)
        elif not check_password_hash(account['password'], password):
            abort(401)
        else:
            await Session.remove(username=username)
            new_session_id = uuid4().hex
            await Session.add(username, new_session_id)

            return json({
                'session_id': new_session_id
            })

blueprint.add_route(LoginView.as_view(), '/')