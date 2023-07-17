from flask_wtf  import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    password_rpt = PasswordField('password_rpt', validators=[DataRequired()])
    account_type = SelectField('account_type', choices=[(0, 'Looking for work'), (1, 'Employer')])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Enter')


    def get_form(self, form_name):
        forms = dict([('name', self.name)
            , ('email', self.email)
            , ('password', self.password)
            , ('password_rpt', self.password_rpt)
            , ('account_type', self.account_type)
            , ('remember_me', self.remember_me)
            , ('submit', self.submit)])
        if form_name in forms.keys():
            return forms[form_name]
        return None



class PersonalData(FlaskForm):
    second_name = StringField('second_name', validators=[Optional()])
    country = StringField('country', validators=[Optional()])
    city = StringField('city', validators=[Optional()])
    birthday = DateField('Start Date', format='%Y-%m-%d',validators=[Optional()])
    gender = SelectField('gender', choices=[(None, ''), ('m', 'male'), ('f', 'female')], validators=[Optional()])
    phone_number = StringField('phone_number', validators=[Optional()])

    def get_form(self, form_name):
        forms = dict([('second_name', self.second_name)
            , ('country', self.country)
            , ('city', self.city)
            , ('birthday', self.birthday)
            , ('gender', self.gender)
            , ('phone_number', self.phone_number)])
        if form_name in forms.keys():
            return forms[form_name]
        return None