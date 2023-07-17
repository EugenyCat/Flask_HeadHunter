from flask import Blueprint


joboffer_blueprint = Blueprint(
    'joboffer_blueprint',
    __name__,
    template_folder='templates',
    static_folder='static'
)


from app.joboffers import routes