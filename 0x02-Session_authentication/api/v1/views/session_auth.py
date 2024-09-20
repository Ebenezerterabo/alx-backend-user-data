#!/usr/bin/env python3
""" Session with Auth class module """
from api.v1.views.auth import Auth
from models.user import User
from uuid import uuid4
from flask import Flask, abort


from flask import Flask, request

app = Flask(__name__)


@app.route('/auth_session/login',
           methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login route
    """
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return "Wrong format"
    if rj.get("email", "") == "":
        return {"error": "email missing"}, 400
    if rj.get("password", "") == "":
        return {"error": "password missing"}, 400
    try:
        user = User.search({"email": rj.get("email")})
    except Exception as e:
        user = None
    if user is None or len(user) == 0:
        return {"error": "no user found for this email"}, 404
    if user[0].is_valid_password(rj.get("password")) is False:
        return {"error": "wrong password"}, 401
    session_id = str(uuid4())
    if session_id not None:
        from api.v1.app import auth
        user[0].session_id = session_id
        user[0].save()
    return {"session_id": session_id}
