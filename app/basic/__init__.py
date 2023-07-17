from flask import Blueprint

basic_blueprint = Blueprint(
    'basic_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from app.basic import routes