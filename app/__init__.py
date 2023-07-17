from flask import Flask, render_template, g
from app.db_postgre.postgre_db import PSQL
from flask_login import current_user
from app.authorization.userlogin import UserLogin


app = Flask(__name__)
app.config.from_object('config')


from app.basic import basic_blueprint
app.register_blueprint(basic_blueprint)

from app.authorization import authorization_blueprint
from app.authorization.routes import login_manager
app.register_blueprint(authorization_blueprint, url_prefix='/login/')

login_manager.init_app(app)
login_manager.login_view = 'authorization_blueprint.login'

from app.joboffers import joboffer_blueprint
app.register_blueprint(joboffer_blueprint, url_prefix='/offers/')


@app.before_request
def before_request():
    g.con_psql = PSQL()
    g.con_psql.create_connection()
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    if g.con_psql is not None:
        return UserLogin().fromDB(user_id, g.con_psql)


@authorization_blueprint.teardown_request
def teardown_request(error):
    if g.con_psql is not None:
        g.con_psql.close_connection()


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page isn\'t found'), 404






