#!/usr/bin/env python3
""" Flask application. """

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Return a message. """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Create a new user. """
    # Get the form data from the request
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # Create a new user
        user = AUTH.register_user(email, password)
        # Return the user's ID
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        # Handle the case where the user already exists
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Create a new session. """
    # Get the form data from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if login is valid
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        # Create a new session
        session_id = AUTH.create_session(email)
        # Set the session cookie
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        # Return the response
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Destroy a session. """
    # Get the session cookie
    session_cookie = request.cookies.get("session_id")
    # Get the user ID from the session cookie
    user_id = AUTH.get_user_from_session_id(session_cookie)
    # Check if the user exits
    if user_id is None:
        abort(403)
    # Destroy the session
    AUTH.destroy_session(user_id.id)
    # Return a response
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Get the user profile. """
    # Get the session cookie
    session_cookie = request.cookies.get("session_id")
    # Get the user ID from the session cookie
    user_id = AUTH.get_user_from_session_id(session_cookie)
    # Check if the user exits
    if user_id:
        # Return the user profile
        return jsonify({"email": user_id.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Get a reset password token. """
    # Get the form data from the request
    email = request.form.get('email')
    # Check if the email is valid
    try:
        # Get the reset token
        reset_token = AUTH.get_reset_password_token(email)
        # Return the reset token
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/update_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update a user's password. """
    # Get the form data from the request
    reset_token = request.form.get('reset_token')
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    # Check if the reset token is valid
    try:
        # Update the user's password
        AUTH.update_password(reset_token, new_password)
        # Return a success message
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
