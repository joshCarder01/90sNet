from flask import (
    jsonify, request
)

from . import commands_blueprint
from .command_result_queue import add_command, pop_command, add_result, get_result
from Backend.common import HandleJSON


COMMAND_NAMES = (
    "machine_up",
    "machine_down",
    "cli"
)


@commands_blueprint.route("/command/results", methods=["GET", "POST"])
def results_interface():
    if request.method == "POST":
        # We are appending a new result to the queue
        
        with HandleJSON():
            add_result(request.json['result'], request.json['id'])
            return "successful\n", 200

    else:
        with HandleJSON():
            return jsonify(get_result(request.json['id']))


@commands_blueprint.route("/command", methods=["GET", "POST"])
def command_interface():
    """
    
    """
    if request.method == "POST":
        with HandleJSON():
            name = request.json['cmd']
            args = request.json.get("args", [])

            return {"id": add_command(name, args)}
    else:
        return jsonify(pop_command())

