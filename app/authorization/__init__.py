from flask import Blueprint


authorization_blueprint = Blueprint(
    'authorization_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from app.authorization import routes