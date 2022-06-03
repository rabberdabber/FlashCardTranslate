from crypt import methods
from . import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort,flash
from .naver_credentials import headers
import requests
from langcodes import *
from .forms import LanguageForm


crud = Blueprint('crud',__name__)
url = "https://openapi.naver.com/v1/papago/n2mt"

@crud.route("/")
def list(error=None):
    page = request.args.get('page', 1, type=int)
    pagination,lists = model.list_categories(page)
    
    form = LanguageForm()
    
    if error is not None:
        form.source.errors = error
        
    return render_template(
        "base.html",
        lists=lists,
        active_list= model.get_list(1),
        pagination=pagination,
        form=form)

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

@crud.route("/list/<int:id>/<string:word>")
def view_word(id,word):
    data = {}
    data['word'] = word
    data['id'] = id
    pagination,todos = model.search_todo(data)
    
    return render_template(
        "search.html",
        lists=todos,
        active_list=model.get_list(id),
        pagination=pagination) 
    


@crud.route('/create/<int:id>', methods=['POST'])
def create(id):
    print("created")
    data = {}
    data['word'] = request.form.get('word')
    if data['word']:
        print(data['word'])
        word = data['word']
        list = model.get_list(id)
        codes = list.code.split("->")
        querystring = {"source":codes[0],"target":codes[1],"text":word}
        response = requests.request("POST", url, headers=headers, params=querystring)

        data['word_translation'] = response.json().get('message').get('result').get('translatedText')
        data['list_id'] = id
        print(data['word_translation'])
        todo = model.create_todo(data)
    
        if todo is None:
            abort(500)
        else:
            return redirect(url_for('.view',id=id))
        
    elif request.form.get('search-word'):
       print(request.form.get("search-word"))
       return redirect(url_for('.view_word',id=id,word=request.form.get('search-word')))
    else:
        return redirect(url_for('.view',id=id))
    
@crud.route('/lists/create', methods=['POST','DELETE'])
def create_list():
  
    form = LanguageForm(request.form)
    if form.validate_on_submit():
        print("submitted and validated")
        print(form.source.data,form.target.data)
        print(form.add.data,form.delete.data,form.search.data)
        
    else:
        print(form.source.data,form.target.data)
        error = ""
        for e in form.source.errors:
            error += e
        # how to pass form into list page ??
        print(error)
        return redirect(url_for('.list'))
        
    src = form.source.data
    target = form.target.data
    src_name = Language.make(language=src).display_name()
    target_name = Language.make(language=target).display_name()
    name = src_name + " -> " + target_name
    id = model.get_id(name) 
    if form.add.data:
        print(request.form.get("search"))
        error = False
        print("gonig oo create list")
        data = {}
        data['name'] = name
        data['code'] = src + "->" + target
        error,body = model.create_list(data)
        if error:
            abort(500)
        else:
            # flash message here
            return redirect(url_for('.list'))
        
    elif form.search.data:
        if id is not None:
            # flash-message for search
            return redirect(url_for('view',id=id))
        
    elif form.delete.data:
        if id is not None:
            # flash-message should be sent to the frontend
            error = model.delete_list(id)
            if error:
                abort(500)
        
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
        
        
