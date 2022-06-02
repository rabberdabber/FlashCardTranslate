from crypt import methods
from . import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort
from .naver_credentials import headers
import requests

crud = Blueprint('crud',__name__)
url = "https://openapi.naver.com/v1/papago/n2mt"

@crud.route("/")
def list():
    '''token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    todos, next_page_token = model.list(cursor=token)'''
    page = request.args.get('page', 1, type=int)
    pagination,lists = model.list_categories(page)

    return render_template(
        "base.html",
        lists=lists,
        todos=model.get_list(14).texts,
        active_list= model.get_list(14),
        pagination=pagination)

@crud.route("/list/<int:id>")
def view(id):
    page = request.args.get('page', 1, type=int)
    pagination,lists = model.list(page,id)
    active_list = model.get_list(id)
    
    return render_template(
        "cards.html",
        lists=lists,
        active_list=active_list,
        pagination=pagination)
    


@crud.route('/create/<int:id>', methods=['POST'])
def create(id):
    print("created")
    data = {}
    
    data['word'] = request.form.get('word')
    word = data['word']
    languages = model.get_languages(id)
    querystring = {"source":languages[0],"target":languages[1],"text":word}
 
    response = requests.request("POST", url, headers=headers, params=querystring)

    data['word_translation'] = response.json().get('message').get('result').get('translatedText')
    data['list_id'] = id
    print(data['word_translation'])
    todo = model.create_todo(data)
   
    if todo is None:
        abort(500)
    else:
        return redirect(url_for('.view',id=id))
    
@crud.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    print("gonig oo create list")
    src = request.form.get('source-language')
    target = request.form.get('target-language')
    error,body = model.create_list(src,target)
    if error:
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
    
@crud.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_list(list_id):
    error = False
    error = model.delete_list(list_id)
    if error:
        abort(500)
    else:
        return jsonify({'success': True})
        
        
