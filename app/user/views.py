import sqlalchemy
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.decorators import login_required
from app.user.forms import UserForm
from app.user.models import User

# Users block
user = Blueprint('user', __name__)


@user.get('/users/')
@login_required
def get_users():
    """
    Get all users
    :return: HTML
    """
    page = request.args.get('page', type=int)
    size = request.args.get('size', type=int, default=0)
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    users = [{'id': item.id, 'username': item.username} for item in pagination]
    vars = {
        'pagination': pagination,
        'users': users,
        'size': size,
    }
    return render_template('user/list.html', **vars)


@user.route('/register/', methods=['GET', 'POST'])
def user_register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        user_to_add = User()
        form.populate_obj(user_to_add)
        try:
            db.session.add(user_to_add)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash('Username already in use.', 'danger')
            return redirect(url_for('user.user_register'))
        flash('User registered. Please, log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('user/register.html', form=form)
