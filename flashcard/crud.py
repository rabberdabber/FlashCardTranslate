from crypt import methods
from . import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort,flash
from .naver_credentials import headers
import requests
#from langcodes import *
from .forms import LanguageForm,WordForm,language_dict


crud = Blueprint('crud',__name__)
url = "https://openapi.naver.com/v1/papago/n2mt"

@crud.route("/")
def list():
    page = request.args.get('page', 1, type=int)
    pagination,lists = model.list_categories(page)
    
    form = LanguageForm() 
        
    return render_template(
        "base.html",
        lists=lists,
        active_list= model.get_list(1),
        pagination=pagination,
        form=form)

@crud.route("/categories/<int:id>/cards",methods=["GET"])
def view(id):
    page = request.args.get('page', 1, type=int)
    pagination,lists = model.list(page,id)
    active_list = model.get_list(id)
    form = WordForm()
    
    return render_template(
        "cards.html",
        lists=lists,
        active_list=active_list,
        pagination=pagination,
        form=form)

@crud.route("/cards/<int:id>",methods=["GET"])
def view_card(id):
    
    data = {}
    pagination,card = model.search_card(id)
    form = WordForm()
    
    return render_template(
        "search.html",
        lists=[card],
        active_list=model.get_list(card.list_id),
        form=form,
        pagination=pagination)
    

@crud.route('/categories/<int:id>/cards', methods=['POST','GET'])
def create_card(id):
    print("created")
    data = {}
    form = WordForm()
    print(form.text.data,form.add.data,form.search.data)
    data['word'] = form.text.data
    
    if form.add.data:
        print(data['word'])
        word = data['word']
        list = model.get_list(id)
        codes = list.code.split("->")
        querystring = {"source":codes[0],"target":codes[1],"text":word}
        response = requests.request("POST", url, headers=headers, params=querystring)
        
        msg = response.json().get('message')
        
        if msg and msg.get('result'):
            data['word_translation'] = msg.get('result').get('translatedText')
        else:
            data['word_translation'] = ":("
        
        data['list_id'] = id
        print(data['word_translation'])
        card = model.create_card(data)
    
        if card is None:
            abort(500)
        else:
            return redirect(url_for('.view',id=id))
        
    elif form.search.data:
        card_id = model.get_card_id(data['word'])
        print(card_id)
        if card_id:
            return redirect(url_for('.view_card',id=card_id))
        else:
            flash('searched word not found')
        
    return redirect(url_for('.view',id=id))
    
@crud.route('/categories', methods=['POST'])
def create_categories():

    form = LanguageForm(request.form)
    if form.validate_on_submit():
        print("submitted and validated")
        print(form.source.data,form.target.data)
        print(form.add.data,form.delete.data,form.search.data)
        
    else:
        print(form.source.data,form.target.data)
        flash("the selected source language should be different from the target language")
        return redirect(url_for('.list'))
        
    src = form.source.data
    target = form.target.data
    src_name = language_dict[src]
    target_name = language_dict[target]
    name = src_name + " -> " + target_name
    id = model.get_id(name) 
    
    if form.add.data:
        print(request.form.get("search"))
        error = False
        print("gonig oo create list")
        data = {}
        data['name'] = name
        data['code'] = src + "->" + target
        
        if id is not None:
            msg = "the category " + name + " already exists, could search it instead"
            flash(msg)
            return redirect(url_for('.list'))
        
        error,body = model.create_list(data)
        
        if error:
            abort(500)
        else:
            msg = "added the new category " + name
            flash(msg)
            
            return redirect(url_for('.list'))
        
    elif form.search.data:
        if id is not None:
            return redirect(url_for('.view',id=id))
        else:
            flash('the category does not exist, you can add it instead')
        
    elif form.delete.data:
        if id is not None:
            return delete_category(id)
        else:
            flash('the category does not exist, you can add it instead')
        
    return redirect(url_for('.list'))
    


@crud.route('/cards/<int:id>', methods=['DELETE'])
def delete(id):
    print("going to delete ",id)
    data = model.delete_card(id)
    
    if data is None:
        abort(500)
    else:
        return data
    
@crud.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    error = False
    name = model.get_list(id).name
    error = model.delete_list(id)
    
    if error:
        abort(500)
    else:
        msg = "successfully deleted the " + name + " category"  
        flash(msg)
        return redirect(url_for('.list'))
        
        
