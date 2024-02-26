from functools import wraps

import jwt
from flask import session, redirect, request, jsonify

from app.config import SECRET_KEY


def login_required(f):
    """
    Decorator to check if user is logged in
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login/')
        return f(*args, **kwargs)

    return wrapper


def token_required(f):
    """
    Decorator to check if token is present and valid
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid!'}), 401
        if current_user not in ['admin', 'user', 'root']:
            return jsonify({'message': 'Wrong user name'}), 401

        return f(*args, **kwargs)

    return wrapper
