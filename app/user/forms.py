from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
