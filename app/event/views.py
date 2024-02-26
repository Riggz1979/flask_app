import datetime

import jwt
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from flask.views import MethodView

from app import db
from app.config import SECRET_KEY
from app.decorators import login_required, token_required
from app.event.forms import EventForm
from app.event.models import Event
from app.event.models import EventUser
from app.user.models import User

# Events block
event = Blueprint('event', __name__)


# Class based views for task 40
class EventListView(MethodView):
    def get(self):
        events = Event.query.all()
        return render_template('class/list.html', items=events, type='event')


class EventDetailView(MethodView):
    def get(self, id):
        event = Event.query.get_or_404(id)
        return render_template('class/detail.html', item=event, type='event')


@event.route('/create/', methods=['POST', 'GET'])
@login_required
def create_event():
    """
    Create a new event
    :return:
    """
    form = EventForm()
    if request.method == 'POST' and form.validate():
        event_to_add = Event()
        form.populate_obj(event_to_add)
        event_to_add.created_by = session.get('user_id')
        try:
            db.session.add(event_to_add)
            db.session.commit()
        except Exception:
            flash('Something wrong...', 'danger')
            return redirect(url_for('event.create_event'))
        flash('Event created.', 'success')
        event_users = EventUser()
        event_users.event_id = event_to_add.id
        event_users.user_id = session.get('user_id')
        event_users.created_at = datetime.date.today()
        event_users.score = 0
        db.session.add(event_users)
        db.session.commit()
        return redirect(url_for('event.get_event_by_id', id=event_to_add.id))
    return render_template('event/create.html', form=form)


@event.get('/events/')
@login_required
def get_events():
    """
    Get all events list
    :return: rendered template (event/list.html)
    """
    # if request.args:
    page = request.args.get('page', type=int)
    size = request.args.get('size', type=int, default=0)
    pagination = Event.query.paginate(page=page, per_page=size, error_out=False)
    events = [{'id': item.id, 'description': item.description} for item in pagination]
    context = {
        'pagination': pagination,
        'events': events,
        'size': size,
        'title': 'Events List'
    }
    return render_template('event/list.html', **context)


@event.get('/search/')
@login_required
def search_event():
    """
    Search events by description
    :return:
    """
    pattern = request.args.get('query')
    if pattern:
        query = db.session.query(Event).where(Event.description == pattern)
        events = db.session.execute(query).scalars()
        context = [{'id': item.id, 'description': item.description} for item in events]
        return render_template('event/list.html', events=context, title='Search result')
    return redirect(url_for('event.get_events')), 302


@event.get('/events/<int:id>/')
@login_required
def get_event_by_id(id):
    """
    Get event by id
    :param id: int
    :return: rendered template (event/detail.html)
    """
    users_list = list()
    query = db.select(Event).where(Event.id == id)
    context = db.session.execute(query).scalar()
    query = db.select(EventUser).where(EventUser.event_id == id)
    users = db.session.execute(query).scalars()
    for item in users:
        users_list.append(item.user_id)
    return render_template('event/detail.html', id=id,
                           context=context, now_date=datetime.date.today(), users_list=users_list)


@event.route('/events/<int:id>/update/', methods=['GET', 'POST'])
@login_required
def update_event(id):
    """
    Edit and update event
    :param id:
    :return:
    """
    form = EventForm()
    query = db.select(Event).where(Event.id == id)
    event_to_update = db.session.execute(query).scalar()
    if request.method == 'GET':
        form.description.data = event_to_update.description
        form.begin_at.data = event_to_update.begin_at
        form.end_at.data = event_to_update.end_at
        form.max_users.data = event_to_update.max_users
        form.is_active.data = event_to_update.is_active
        form.created_by = session.get('user_id')
        return render_template('event/update.html', form=form, id=event_to_update.id)
    else:
        try:
            form.populate_obj(event_to_update)
            event_to_update.created_by = session.get('user_id')
            db.session.add(event_to_update)
            db.session.commit()
        except Exception:
            flash('An error occurred', category='danger')
            return redirect(url_for('event.update_event', id=event_to_update.id))
        flash('Event updated.', 'success')
        return redirect(url_for('event.get_event_by_id', id=event_to_update.id))


@event.get('/events/<int:id>/users/')
@login_required
def get_users_by_event_id(id):
    """
    Get users by event id
    :param id:
    :return: rendered template (event/users.html)
    """
    query = db.select(EventUser).where(EventUser.event_id == id)
    users = db.session.execute(query).scalars()
    context = [{'id': item.user_id,
                'username': item.user.username} for item in users]
    return render_template('event/users.html', id=id, event_users=context)


@event.post('/events/<int:id>/users')
@login_required
def bind_user_by_event_id(id):
    """
    Bind user to selected ivent
    :param id:
    :return:
    """
    user_to_add = EventUser()
    user_to_add.event_id = id
    user_to_add.user_id = session.get('user_id')
    user_to_add.created_at = datetime.date.today()
    user_to_add.score = 0
    try:
        db.session.add(user_to_add)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Something went wrong...', 'danger')
        return redirect(url_for('event.get_event_by_id', id=id))
    flash('User bound.', 'success')
    return redirect(url_for('event.get_users_by_event_id', id=id))


# API section
@event.post('/api/events/')
@token_required
def create_event_by_api():
    """
    Create new event (API)
    :return: Test...
    """
    return jsonify(request.json), 201


@event.patch('/api/events/<int:id>/')
@token_required
def update_event_by_api(id):
    """
    Update event by id (API)
    :param id: int
    :return: Test...
    """
    return jsonify(request.json), 200


@event.delete('/api/events/<int:id>/')
@token_required
def delete_event(id):
    """
    Delete event by id (API)
    :param id: int
    :return: Test...
    """
    return "", 204


@event.get('/api/users/')
@token_required
def get_users_by_api():
    """
    Get all users list (API)
    :return: Test...
    """
    page = request.args.get('page', type=int)
    size = request.args.get('size', type=int, default=0)
    users = User.query.paginate(page=page, per_page=size, error_out=False)
    context = [{'id': item.id,
                'first_name': item.first_name,
                'last_name': item.last_name,
                'username': item.username} for item in users]
    return jsonify(context), 200


@event.get('/api/events/')
@token_required
def get_events_by_api():
    """
    Get all users list (API)
    :return: Test...
    """
    page = request.args.get('page', type=int)
    size = request.args.get('size', type=int, default=0)
    events = Event.query.paginate(page=page, per_page=size, error_out=False)
    context = [{
        'id': item.id,
        'description': item.description,
        'created_by': item.created_by,
        'begin_at': item.begin_at,
        'end_at': item.end_at,
        'max_users': item.max_users,
        'is_active': item.is_active
    } for item in events]
    return jsonify(context), 200


@event.post('/api/users/')
@token_required
def create_user():
    """
    Create a new user (API)
    :return: Test...
    """
    return jsonify(request.json), 201


@event.post('/api/users/<int:id>/')
@token_required
def update_user(id):
    """
    Update a user (API)
    :param id: int
    :return: Test...
    """
    return jsonify(request.json), 201


@event.patch('/api/users/<int:id>/')
@token_required
def edit_user(id):
    """
    Edit a user (API)
    :param id: int
    :return: Test...
    """
    return jsonify(request.json), 200


@event.delete('/api/users/<int:id>/')
@token_required
def delete_user(id):
    """
    Delete a user (API)
    :param id: int
    :return: Test...
    """
    return "", 204


@event.post('/api/login/')
def api_login():
    """
    Create an auth token for API login
    :return: JSON (token)
    """
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({"error:": "invalid username or password"}), 401
    token = jwt.encode({
        'user': auth.get('username'),
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=60)
    }, SECRET_KEY)
    return jsonify({"token": token}), 200


@event.get('/api/events/<int:id>/users/')
@token_required
def api_get_users_by_event_id(id):
    """
    Get event users by event id
    :param id: int
    :return: JSON
    """
    query = db.select(EventUser).where(EventUser.event_id == id)
    users = db.session.execute(query).scalars()
    context = [{'id': item.id,
                'user_id': item.user_id,
                'event_id': item.event_id,
                'created_at': item.created_at,
                'username': item.user.username} for item in users]
    return jsonify(context), 200
