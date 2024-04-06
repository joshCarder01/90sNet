
from .Events import events_blueprint as events_blueprint
from .Users import users_blueprint as users_blueprint
from .Machines import machines_blueprint as machines_blueprint
from .Commands import commands_blueprint as commands_blueprint

# Make it somewhat easier to register everything with the main flask app
blueprints = (
    events_blueprint,
    users_blueprint,
    machines_blueprint,
    commands_blueprint
)

