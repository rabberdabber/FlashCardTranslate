
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
    __tablename__ = "texts"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(), nullable=False)
    word_translation = db.Column(db.String(),nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'lists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, word: {self.word}, translation: {self.word_translation}>'

class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    texts = db.relationship('Text', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList ID: {self.id}, name: {self.name}, todos: {self.todos}>'
    
'''def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Todo.query
             .order_by(Todo.id)
             .limit(limit)
             .offset(cursor))
    todos = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(todos) == limit else None
    return (todos, next_page)'''
 
def list(page,id,limit=8):
    pagination = Text.query.filter_by(list_id=id).paginate(page=page,per_page=limit)
    todos_list = builtin_list(map(from_sql, pagination.items))
    return pagination,todos_list

def list_categories(page,limit=5):
    pagination = List.query.paginate(page=page,per_page=limit)
    list = builtin_list(map(from_sql, pagination.items))
    return pagination,list
        
def get_lists():
    return List.query.all()

def get_list(id):
    return List.query.get(id)

def get_id(name):
    list = List.query.filter_by(name=name).first()
    return list.id if list is not None else None

def create_todo(data):
    todo = None
    try:
        todo = Text(**data)
        db.session.add(todo)
        db.session.commit()
    except:
        todo = None
        db.session.rollback()
        print(sys.exc_info())

    return todo

def search_todo(data):
    todos = None
    pagination = Text.query.filter_by(list_id=data['id']).filter_by(word=data['word']).paginate(page=1,per_page=5)
    todos = builtin_list(map(from_sql, pagination.items))
    return pagination,todos

def create_list(data):
    error = False
    body = {}
    try:
        list = List(**data)
        db.session.add(list)
        db.session.commit()
        body['id'] = list.id
        body['name'] = list.name
        body['code'] = list.code
    except:
        db.session.rollback()
        error = True
        body = None
        print(sys.exc_info)
    finally:
        db.session.close()
    
    return error,body
   

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

def delete_list(list_id):
    error = False
    try:
        list = List.query.get(list_id)
        for text in list.texts:
            db.session.delete(text)

        db.session.delete(list)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    
    return error
   


def _create_database():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")
    
