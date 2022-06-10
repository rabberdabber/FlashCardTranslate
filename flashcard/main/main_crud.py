from crypt import methods
from flashcard import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort,flash,session
from .naver_credentials import headers
import requests
#from langcodes import *
from flashcard.forms import LanguageForm,WordForm,language_dict
from flashcard.auth.authentication import AUTH0_AUDIENCE,AUTH0_DOMAIN,AUTH0_CLIENTID, AuthError, get_token_auth_header,verify_decode_jwt,requires_login
from . import main
from urllib.parse import urlencode

import sys
sys.path.append('../')
from config import Config


url = "https://openapi.naver.com/v1/papago/n2mt"


# helper functions
@main.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Not found",
    }),404
    
@main.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'message':'Invalid or Inconsistent request'
         }),400
    
@main.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': "Internal server error",
    }),500
    

def get_translation(data,id):
    list = model.get_list(id)
    codes = list.code.split("->")
    querystring = {"source":codes[0],"target":codes[1],"text":data['word']}
    response = requests.request("POST", url, headers=headers, params=querystring)

    msg = response.json().get('message')

    data['list_id'] = id
    data['word_translation'] =":("
    
    if msg and msg.get('result'):
        data['word_translation'] = msg.get('result').get('translatedText')
    
   
        
''' Resource Endpoints (HTML)'''

@main.route('/categories', methods=['GET'])
@requires_login()
def list():
    page = request.args.get('page', 1, type=int)
    print('before session list_categories ',session['sub'])
    pagination,lists = model.list_categories(page)
     
    form = LanguageForm() 
        
    return render_template(
        "base.html",
        lists=lists,
        active_list= model.get_list(1),
        pagination=pagination,
        form=form)

@main.route("/categories/<int:id>/cards",methods=["GET"])
@requires_login()
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


@main.route("/cards/<int:id>",methods=["GET"])
@requires_login()
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


@main.route('/categories/<int:id>/cards', methods=['POST'])
@requires_login()
def create_card(id):
    print("created")
    data = {}
    form = WordForm()
    data['word'] = form.text.data
    
    if form.add.data:
        print(data['word'])
        get_translation(data,id)
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

    
@main.route('/categories', methods=['POST'])
@requires_login()
def create_categories():
    form = LanguageForm(request.form)
    
    if not form.validate_on_submit():
        flash("the selected source language should be different from the target language")
        return redirect(url_for('.list')) 
   
    src = form.source.data
    target = form.target.data
    src_name = language_dict[src]
    target_name = language_dict[target]
    name = src_name + " -> " + target_name
    id = model.get_id(name) 
    
    if form.add.data:
        error = False
        data = {}
        data['name'] = name
        data['code'] = src + "->" + target
        data['owner'] = session['sub']
        print(data['owner'])
        
        if id is not None:
            msg = "the category " + name + " already exists, could search it instead"
            flash(msg)
            return redirect(url_for('.list'))
        
        error,_ = model.create_list(data)
        
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
    
    
@main.route('/cards/<int:id>', methods=['DELETE'])
@requires_login()
def delete(id):
    print("going to delete ",id)
    error = model.delete_card(id)
    
    if error:
        abort(500)
    else:
        return jsonify({'success':True})

        
@main.route('/categories/<int:id>', methods=['DELETE'])
@requires_login()
def delete_category(id):
    error = False
    list = model.get_list(id)
    print(list)
    name = list.name
    error = model.delete_list(id)
    
    if error:
        abort(500)
    else:
        msg = "successfully deleted the " + name + " category"  
        flash(msg)
        return jsonify({'success':True})
        
        

