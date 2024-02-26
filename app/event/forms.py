from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class EventForm(FlaskForm):
    description = StringField(label='Description', validators=[DataRequired()])
    begin_at = DateField(label='Start Date', validators=[DataRequired()], default=date.today)
    end_at = DateField(label='Deadline Date', validators=[DataRequired()], default=date.today)
    max_users = IntegerField(label='Max Users', validators=[DataRequired(), NumberRange(1)], default=1)
    is_active = BooleanField(label='Active', default=True)
