from flask_wtf  import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class OfferForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    skills = StringField('skills', validators=[DataRequired()])
    submit = SubmitField('Create')

    def get_form(self, form_name):
        forms = dict([('title', self.title)
            , ('description', self.description)
            , ('skills', self.skills)])
        if form_name in forms.keys():
            return forms[form_name]
        return None