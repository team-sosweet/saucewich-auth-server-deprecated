from uuid import uuid4

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from werkzeug.security import check_password_hash

from app.models.account import Account
from app.models.session import Session

blueprint = Blueprint('logout-api', url_prefix='/logout')

class LogoutView(HTTPMethodView):
    async def post(self, request: Request):
        session_id: str = request.json['session_id']

        if not await Session.exists(session_id=session_id):
            abort(401)

        await Session.remove(session_id=session_id)
        return json({
            'success': True
        })

blueprint.add_route(LogoutView.as_view(), '/')