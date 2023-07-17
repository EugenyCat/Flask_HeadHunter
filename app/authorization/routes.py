from app.authorization import authorization_blueprint
from flask import render_template, request, flash, redirect, url_for, g, get_flashed_messages, session
from app.authorization.forms import LoginForm, PersonalData
from app.authorization.dao import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from app.authorization.userlogin import UserLogin

MAX_CONTENT_LENGTH = 1024 * 1024 * 5

login_manager = LoginManager()


@authorization_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        session.pop('_flashes', None)
        return redirect(url_for('authorization_blueprint.profile'))
    form = LoginForm()
    if request.method == 'POST':
        user = g.con_psql.get_by_email(request.form['email'])
        if user and user.login_check_password_hash(request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if 'remember_me' in request.form.keys() else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('authorization_blueprint.profile'))
    inputs = ['email', 'password', 'remember_me']   #in DB
    return render_template('authorization.html', form=form, title='Sign in', input=inputs)


@authorization_blueprint.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = LoginForm()
    if request.method == 'POST':
        user = User(None, request.values.get('name'), request.values.get('email'), request.values.get('password'), request.values.get('account_type'))
        if g.con_psql.get_by_email(user.email) is None:
           if user.registration_check_user_params(request.values.get('password_rpt')) and form.validate_on_submit():
                g.con_psql.insert_user_in_db(user)
                session.pop('_flashes', None)
                return redirect('/')
    inputs = ['email', 'password', 'password_rpt', 'account_type']  #in DB
    return render_template('registration.html', form=form, title='Registration', input=inputs)


@authorization_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You go out from profile')
    return redirect(url_for('authorization_blueprint.login'))


@authorization_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    session['url'] = url_for('authorization_blueprint.profile')

    if request.method == 'POST':
        g.con_psql.delete_joboffer_rec(request.values.get("delete"))

    user_offers_link = g.con_psql.get_user_offers_links(g.user.get_id())

    return render_template('profile.html', user_offers=user_offers_link)


@authorization_blueprint.route('/profile/edit')
@login_required
def profile_edit():
    pd_form = PersonalData(gender=current_user.get_person_data()['gender'])
    m_form = LoginForm()
    add_inputs = ['country', 'city', 'birthday', 'gender', 'phone_number']  # in DB
    main_inputs = ['name', 'second_name']  # in DB
    return render_template('profile_edit.html', form_main=m_form, form_additional=pd_form, add_inputs=add_inputs, main_inputs=main_inputs)


@authorization_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['profile_photo']
        if file:
            file_name = current_user.get_id()
            file.save(f'app\\static\\avatars_jpeg\\{file_name}.jpg')
            g.con_psql.update_avatar(current_user.get_id(), f'../../static/avatars_jpeg/{file_name}.jpg')
        else:
            print('Some Error')

        g.con_psql.update_user_personal(current_user.get_id(),
                                      request.values.get('name') or None,
                                      request.values.get('second_name') or None,
                                      request.values.get('country') or None,
                                      request.values.get('city') or None,
                                      request.values.get('birthday') or None,
                                      None if request.values.get('gender') == 'None' else request.values.get('gender'),
                                      request.values.get('phone_number') or None)


    return redirect(url_for('authorization_blueprint.profile'))