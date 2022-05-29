from crypt import methods
from . import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort

crud = Blueprint('crud',__name__)

@crud.route("/")
def list():
    '''token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    todos, next_page_token = model.list(cursor=token)'''
    page = request.args.get('page', 1, type=int)
    pagination,todos_list = model.list(page)

    return render_template(
        "base.html",
        todos=todos_list,
        pagination=pagination)
    
@crud.route('/<id>')    
def view(id):
    return None

@crud.route('/create', methods=['POST'])
def create():
   print("created")
   data = {}
   description = request.form.get('description')
   print(description)
   data['description'] = description
   failed = model.create_todo(description)
  
   if failed:
       abort(500)
   else:
       return redirect(url_for('.list'))

@crud.route('/<todo_id>/set-completed', methods=['POST'])
def update(todo_id):
    completed = request.get_json()['completed']
    todo = model.update_todo(todo_id,completed)
    
    if todo is None:
        abort(500)
    else:
        return redirect(url_for("index"))
    

@crud.route('/<todo_id>/delete', methods=['DELETE'])
def delete(todo_id):
    print("going to delete ",todo_id)
    data = model.delete_todo(todo_id)
    
    if data is None:
        abort(500)
    else:
        return data
        
        
