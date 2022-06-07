from crypt import methods
from . import model
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, json, abort,flash
from .naver_credentials import headers
import requests
#from langcodes import *
from .forms import LanguageForm,WordForm,language_dict


crud = Blueprint('crud',__name__)
url = "https://openapi.naver.com/v1/papago/n2mt"

# helper functions
@crud.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Not found",
    }),404

@crud.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'message':'Invalid or Inconsistent request'
         }),400
    
@crud.errorhandler(500)
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
    
   
        
def card_response_json(card):
    response = {'success':True,'message':'card added successfully'}
    response['card'] = card.to_json()
    return jsonify(response),201

def create_card_json(word,id):
    data = {}
    data['word'] = word
    get_translation(data,id)
    card = model.create_card(data)
    return card_response_json(card)


''' Resource Endpoints '''
@crud.route('/categories/<int:id>/json', methods=['GET'])
def get_category(id):    
    category = model.get_list(id)
    if category:
        return jsonify(category.to_json())
    else:
        return not_found(None)


@crud.route('/categories/json', methods=['GET'])
@crud.route("/json",methods=['GET'])
def list_json():
    page = request.args.get('page', 1, type=int)
    pagination,_ = model.list_categories(page)
    
    categories = [category.to_json() for category in pagination.items]
    prev = url_for('crud.list', page=page-1) if pagination.has_prev else None
    next = url_for('crud.list', page=page+1) if pagination.has_next else None
    
    return jsonify({
        'categories': categories,
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'total_pages': pagination.pages,
        'message': 'category list retrieved successfully',
        'success':True
    })


@crud.route('/categories/', methods=['GET'])
@crud.route("/",methods=['GET'])
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


@crud.route("/categories/<int:id>/cards/json",methods=["GET"])
def view_json(id):
    page = request.args.get('page', 1, type=int)
    pagination,_ = model.list(page,id)
  
    cards = [card.to_json() for card in pagination.items]
    prev = url_for('crud.list', page=page-1) if pagination.has_prev else None
    next = url_for('crud.list', page=page+1) if pagination.has_next else None
    
    return jsonify({
        'cards': cards,
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'total_pages': pagination.pages      
    })
    

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


@crud.route("/cards/<int:id>/json",methods=["GET"])
def view_card_json(id):
    page = request.args.get('page', 1, type=int)  
    
    if model.get_card(id):
        pagination,_ = model.search_card(id)
        card = [card.to_json() for card in pagination.items][0]
        prev = url_for('crud.list', page=page-1) if pagination.has_prev else None
        next = url_for('crud.list', page=page+1) if pagination.has_next else None
        
        return jsonify({
            'categories': card,
            'prev_url': prev,
            'next_url': next,
            'count': pagination.total,
            'total_pages': pagination.pages,
        }) 
    else:
        return not_found(None)
    
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

@crud.route('/cards/json', methods=['POST'])
def create_cards_json():
    word = request.json.get('word')
    category_id = request.json.get('category_id')
    if not request.json or word is None or category_id is None:
        return bad_request(None)
    else:
        category = model.get_list(category_id)
        if not category:
            return not_found(None)
        
        return create_card_json(word,category_id)

        
@crud.route("/categories/<int:id>/cards/json",methods=["POST"])
def append_card_json(id):
    category = model.get_list(id)
    word = request.json.get('word')
    if not category:
        return not_found(None)
    else:
        if not request.json or not word:
            return bad_request(None)
        
        return create_card_json(word,id)


@crud.route('/categories/<int:id>/cards', methods=['POST'])
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


@crud.route('/categories/json', methods=['POST'])
def create_categories_json():
    if request.json:
        data = request.json
        result,error = model.List.from_json(data)
        if not error:
            print(result)
            return jsonify(result.to_json()),201
        else:
            result["success"] = False
            if result['message'] == 'category already exists':
                return jsonify(result),409
            return bad_request(400)
    
    
@crud.route('/categories', methods=['POST'])
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
    

@crud.route('/cards/<int:id>/json', methods=['DELETE'])
def delete_cards_json(id):
    data = model.delete_card(id)
    
    if data is None:
        return not_found(None)
    else:
        return jsonify({'success':True,'message': 'card deleted'}),204
    
@crud.route('/cards/<int:id>', methods=['DELETE'])
def delete(id):
    print("going to delete ",id)
    error = model.delete_card(id)
    
    if error:
        abort(500)
    else:
        return jsonify({'success':True})

@crud.route('/categories/<int:id>/json', methods=['DELETE'])
def delete_categories_json(id):
    error = model.delete_list(id)
    
    if error:
        return not_found(None)
    else:
        return jsonify({'success':True,'message': 'category deleted'}),204
        
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
        return jsonify({'success':True})
        
        
