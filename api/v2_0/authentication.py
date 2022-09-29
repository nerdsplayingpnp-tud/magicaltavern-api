import logging
import uuid

from api.v2_0.models import dbsql as db
from api.v2_0.models import Devices
from main import app


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


def validate_token(token: str) -> bool:
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
            print("Checking token " + str(dbtoken.key))
            if dbtoken.key == token:
                return True
        return False
    else:
        logging.error("token-attribute cannot be empty.")


def remove_token(token: str = None, name: str = None):
    """Removes (invalidates) an access token. Only one argument 'token' OR 'name' can be passed,
    not both.

    Args:
        token (str): The token to be invalidated.
        name (str): The name of the token to be invalidated.

    Returns:
        Nothing
    """
    if token != None and name != None:
        logging.error("Only one argument 'name' OR 'token' can be passed.")
        return
    if name != None and name != "":
        with app.app_context():
            devices = Devices.query.all()
        for device in devices:
            if device.name == name:
                with app.app_context():
                    db.session.remove(device)
                    return db.session.commit()
    elif token != None and token != "":
        with app.app_context():
            devices = Devices.query.all()
        for device in devices:
            if device.key == token:
                with app.app_context():
                    db.session.remove(device)
                    return db.session.commit()
    else:
        return logging.error(
            "The token that was supposed to be removed could not be found."
        )
