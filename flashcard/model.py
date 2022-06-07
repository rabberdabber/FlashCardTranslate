
from enum import unique
from flask import Flask, request, abort, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from .forms import codes,languages

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
        return f'<Text ID: {self.id}, word: {self.word}, translation: {self.word_translation}>'
    
    def to_json(self):
        return {
            'self_url': url_for('crud.view_card', id=self.id),
            'categories_url': url_for('crud.view', id=self.list_id),
            'word': self.word,
            'id': self.id,
            'category_name': get_list(self.list_id).name,
            'translation': self.word_translation
        }

class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    texts = db.relationship('Text', backref='list', lazy=True)

    def __repr__(self):
        return f'<List ID: {self.id}, name: {self.name}, texts: {self.texts}>'
    
    def to_json(self): 
        languages = self.name.split('->')
        return {
            'self_url': url_for('crud.get_category', id=self.id),
            'source': languages[0],
            'target': languages[1],
            'id': self.id,
            'cards_url': url_for('crud.view_json', id=self.id),
            'cards_count': len(self.texts)
        }
    
    def from_json(json_category):
        source = json_category.get('source')
        target = json_category.get('target')
        
        if source is None or target is None or not source in languages or not target in languages:
            return {'message': 'unsupported language'},True
        
        name = source + " -> " + target
        src_index = languages.index(source)
        target_index = languages.index(target)
        code = codes[src_index] + "->" + codes[target_index]
        id = get_id(name)
        
        if id is not None:
            return {'message': 'category already exists'},True
        
        data = {}
        data['name'] = name
        data['code'] = code
        
        error,list = create_list(data)
        
        if error:
            return {'message': 'error creating category'},True
            
        return list,False
    

def list(page,id,limit=8):
    pagination = Text.query.filter_by(list_id=id).paginate(page=page,per_page=limit)
    cards_list = builtin_list(map(from_sql, pagination.items))
    return pagination,cards_list

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

def get_name(id):
    name = Text.query.get(id).word
    return name

def get_card_id(word):
    return Text.query.filter_by(word=word).first().id

def get_card(id):
    return Text.query.get(id)

def create_card(data):
    text = None
    try:
        text = Text(**data)
        db.session.add(text)
        db.session.commit()
    except:
        text = None
        db.session.rollback()
        print(sys.exc_info())

    return text

def search_card(id):
    text = None
    card = Text.query.get(id)
    pagination = Text.query.filter_by(id=id).paginate(page=1,per_page=5)
    return pagination,card

def create_list(data):
    error = False
    body = {}
    try:
        list = List(**data)
        db.session.add(list)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        body = None
        print(sys.exc_info)
    
    return error,list
   

def delete_card(id):
    error = False
    try:
        text = Text.query.get(id)
        db.session.delete(text)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    
    return error

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
    
    return error
   

def _create_database():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")
    
