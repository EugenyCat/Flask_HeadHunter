from app.basic import basic_blueprint
from flask import render_template, request, session
import app.utils.utils as utils


#Create views
@basic_blueprint.route('/')
@basic_blueprint.route('/index/')
def index():
    return render_template('index.html')


@basic_blueprint.route('/candidates/')
def candidate_list():
    candidates = utils.load_candidates_from_json()
    return render_template('candidates_list.html', candidates=candidates)


@basic_blueprint.route('/candidate/<int:uid>')
def candidate_information(uid):
    candidate = utils.get_candidate(uid)
    return render_template('candidate_information.html', candidate=candidate)


@basic_blueprint.route('/candidate/search/', methods=['POST'])
def candidate_search_by_name():
    candidate_name =    request.form['search_candidate_name']
    candidates = utils.get_candidate_by_name(candidate_name)
    return render_template('candidate_search_by_name.html', candidates=candidates, len_candidates = len(candidates))


@basic_blueprint.route('/skills/')
def skills_list():
    skills = utils.get_skills_list()
    return render_template('skills_list.html', skills=skills)


@basic_blueprint.route('/skills/search/', methods=['POST'])
def candidates_by_skills():
    skill=request.form['search_skill']
    candidates = utils.get_candidate_by_skill(skill)
    return render_template('candidates_by_skills.html', candidates=candidates, len_candidates = len(candidates))



data = [1, 2, 3, 4]
@basic_blueprint.route('/session/')
def session_data():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True
    return f"<p>session['data']: {session['data']}"


