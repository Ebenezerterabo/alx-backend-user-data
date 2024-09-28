#!/usr/bin/env python3
""" Flask application. """

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Return a message. """
    AUTH = Auth()
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
        if user is None:
            return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        # Return an error message
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
