import logging
import uuid

from api.v2_0.models import dbsql as db
from api.v2_0.models import Devices
from flask import request, abort, Blueprint
from main import app

authentication = Blueprint("auth_api_v2", __name__)


@authentication.route("/api/v2.0/auth", methods=["GET", "POST", "PUT", "DELETE"])
def test_authentication():
    abort_if_token_invalid(request)
    return "Success.", 200


def create_token(name: str) -> str:
    """Creates a new API access token which is stored in the database under a given name.

    Args:
        name (str): The name of the application you want an api key for. Error, if not unique or empty.

    Returns:
        str: The created API access token as a String.
    """
    if name != None and name != "":
        with app.app_context():
            devices = Devices.query.all()
            for device in devices:
                if device.name == name:
                    return logging.error(
                        "Specified name-attribute is already present in the database. Duplicates are not allowed. Aborted."
                    )
    else:
        logging.error("name-attribute cannot be empty.")
    key = str(uuid.uuid4().hex)
    with app.app_context():
        db.session.add(Devices(key=key, name=name))
        db.session.commit()
    return key


def abort_if_token_invalid(request: request) -> None:
    """unlike request_has_valid_token, this function, if called from the context of a flask route,
    will abort a request with a status 401 response, if the supplied request does not have a valid
    API token in its' header.

    Args:
        request (request): A flask request object

    Returns:
        None: This function either terminated by returning NoneType if the request has a valid API
        Token in its' header, or by aborting the request with an HTTP 401 status code.
    """
    if request_has_valid_token(request):
        return None
    else:
        abort(401)


def request_has_valid_token(request: request) -> bool:
    """If passed a flask request object, this method will check whether or not the provided API
    token exists and is valid, and will then return a corresponding bool.

    Args:
        request (request): A flask request object.

    Returns:
        bool: True, if the token has been verified to be valid.. False, if not.
    """
    if request.headers.get("token") and __validate_token(request.headers.get("token")):
        return True
    return False


def __validate_token(token: str) -> bool:
    """Checks if a given token is valid for accessing the API.

    Args:
        token (str): The token to check

    Returns:
        bool: True, if the passed access token is valid. False, if it isn't.
    """
    if token != None and token != "":
        with app.app_context():
            tokens = Devices.query.all()
        for dbtoken in tokens:
            if dbtoken.key == token:
                return True
        return False
    return False


def remove_token(name: str = None):
    """Removes (invalidates) an access token.

    Args:
        name (str): The name of the token to be invalidated.

    Returns:
        Nothing
    """
    if name == None or name == "":
        return logging.error("name-attribute cannot be empty.")
    with app.app_context():
        keys = Devices.query.all()
    for key in keys:
        if key.name == name:
            with app.app_context():
                db.session.delete(key)
                db.session.commit()
            return
