import datetime

from flask import (
    jsonify, request, current_app
)
from sqlalchemy import select

from typing import NamedTuple

from Backend.Models import Machine
from Backend import db
from Backend.common import NamedTupleEncoder

from . import commands_blueprint
from .command_result_queue import add_command, pop_command, add_result, get_all_results


COMMAND_NAMES = (
    "machine_up",
    "machine_down",
    "cli"
)


@commands_blueprint.route("/command/results", methods=["GET", "POST"])
def results_interface():
    if request.method == "POST":
        # We are appending a new result to the queue
        if request.json:
            add_result(request.json['result'], request.json['id'])
            return "successful\n", 200
        else:
            return "Requires JSON", 400
    else:
        return jsonify(get_all_results())


@commands_blueprint.route("/command", methods=["GET", "POST"])
def command_interface():
    """
    
    """
    if request.method == "POST":
        if request.json:
            name = request.json['cmd']
            args = request.json.get("args", None)

            return {"id": add_command(name, args)}
        else:
            return "Need JSON", 400
    else:
        return jsonify(pop_command())


# Send the command to the manager to bring the given machine name up
#
# Will set up the command to be slotted into a queue
# @commands_blueprint.route("/command/machine/up", methods=["POST"])
# def bring_up_container():
#     if request.json:
#         args = request.json.get("args", None)
#         if args is None:
#             return "JSON Requires key `args`", 400
        
#         # Now we submit to the job queue
#         return {"id": add_command(COMMAND_NAMES[0], args)}
#     else:
#         return "Need JSON", 400


# @commands_blueprint.route("/command/machine/down", methods=["POST"])
# def bring_down_container():
#     if request.json:
#         args = request.json.get("args", None)
#         if args is None:
#             return "JSON Requires key `args`", 400
        
#         # Now we submit to the job queue
#         return {"id": add_command(COMMAND_NAMES[1], args)}
#     else:
#         return "Need JSON", 400
