# Handle a variety of Exceptions which may occur which should not return a 500
from flask import (
    Flask,
)

from Backend.exceptions import MissingJSONKey


def handle_json_key_errors(app: Flask):
    def handling_json_key_error(e: MissingJSONKey):
        return e.message, 400
    
    app.register_error_handler(MissingJSONKey, handling_json_key_error)

    return

def generic_500_handler(app: Flask):
    # Enables a nicer handling of applicaiton errors

    def handle_500_errors(e):
        return "There was an internal server error!\n", 500
    
    app.register_error_handler(500, handle_500_errors)


def register_error_handlers(app: Flask):

    # handle_json_key_errors(app)
    generic_500_handler(app)
