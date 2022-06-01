
from enum import unique
from flask import Flask, request, abort, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

builtin_list = list
db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)
    
def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

class Text(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(), nullable=False)
    word_translation = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}, completed: {self.completed}>'


'''def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Todo.query
             .order_by(Todo.id)
             .limit(limit)
             .offset(cursor))
    todos = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(todos) == limit else None
    return (todos, next_page)'''
 
def list(page,limit=8):
    pagination = Text.query.paginate(page=page,per_page=limit)
    todos_list = builtin_list(map(from_sql, pagination.items))
    return pagination,todos_list
        

def create_todo(data):
    error = False
    try:
        todo = Text(**data)
        db.session.add(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    return error
   

def read(todo_id):
    return None

def update_todo(todo_id,completed):
    todo = None
    try:
        todo = Text.query.get(todo_id)
        print('Todo: ', todo)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
   
    
    return from_sql(todo) if todo is not None else None
    

def delete_todo(todo_id):
    error = False
    try:
        todo = Text.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    
    return {'success': True} if not error else None




def _create_database():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")
    
