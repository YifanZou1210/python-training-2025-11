from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from store_locator.app.models import User

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request(refresh=False)

        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or user.status != 'active':
            return jsonify({'error': 'User not found or inactive'}), 401

        return fn(current_user=user, *args, **kwargs)

    return wrapper


def permission_required(permission_name):
    def decorator(fn):
        @wraps(fn)
        @jwt_required_custom
        def wrapper(current_user, *args, **kwargs):
            if not current_user.has_permission(permission_name):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required': permission_name
                }), 403

            return fn(current_user=current_user, *args, **kwargs)

        return wrapper
    return decorator
