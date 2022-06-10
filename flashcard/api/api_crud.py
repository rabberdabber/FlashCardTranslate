from unicodedata import category
from flask import Flask,Blueprint, jsonify, redirect, render_template, request, url_for, json, abort,flash
from flashcard import model
from flashcard.auth.authentication import AuthError,requires_auth
from flashcard.main.main_crud import get_translation
from . import api


# helper functions
@api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Not found",
    }),404

@api.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'message':'Invalid or Inconsistent request'
         }),400
    
@api.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': "Internal server error",
    }),500
    
@api.errorhandler(AuthError)
def auth_error(e):
    return e.error,e.status_code
    
'''Helper Functions '''

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


''' JSON API implementation '''

@api.route('/categories/<int:id>/json', methods=['GET'])
@requires_auth('read:category')
def get_category(payload,id):    
    category = model.get_list(id)
    if category:
        return jsonify(category.to_json())
    else:
        return not_found(None)
    
    
@api.route('/categories/json', methods=['GET'])
@api.route("/json",methods=['GET'])
@requires_auth('read:category')
def list_json(payload):
    page = request.args.get('page', 1, type=int)
    pagination,_ = model.list_categories(page)
    
    categories = [category.to_json() for category in pagination.items]
    prev = url_for('main.list', page=page-1) if pagination.has_prev else None
    next = url_for('main.list', page=page+1) if pagination.has_next else None
    
    return jsonify({
        'categories': categories,
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'total_pages': pagination.pages,
        'message': 'category list retrieved successfully',
        'success':True
    })


@api.route("/categories/<int:id>/cards/json",methods=["GET"])
@requires_auth('read:card')
def view_json(payload,id):
    page = request.args.get('page', 1, type=int)
    pagination,_ = model.list(page,id)
  
    cards = [card.to_json() for card in pagination.items]
    prev = url_for('main.list', page=page-1) if pagination.has_prev else None
    next = url_for('main.list', page=page+1) if pagination.has_next else None
    
    return jsonify({
        'cards': cards,
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total,
        'total_pages': pagination.pages      
    })
    
@api.route("/cards/<int:id>/json",methods=["GET"])
@requires_auth('read:card')
def view_card_json(payload,id):
    page = request.args.get('page', 1, type=int)  
    
    if model.get_card(id):
        pagination,_ = model.search_card(id)
        card = [card.to_json() for card in pagination.items][0]
        prev = url_for('main.list', page=page-1) if pagination.has_prev else None
        next = url_for('main.list', page=page+1) if pagination.has_next else None
        
        return jsonify({
            'categories': card,
            'prev_url': prev,
            'next_url': next,
            'count': pagination.total,
            'total_pages': pagination.pages,
        }) 
    else:
        return not_found(None)
    

@api.route('/categories/json', methods=['POST'])
@requires_auth('create:category')
def create_categories_json(payload):
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
        
        
@api.route('/cards/json', methods=['POST'])
@requires_auth('create:card')
def create_cards_json(payload):
    word = request.json.get('word')
    category_id = request.json.get('category_id')
    if not request.json or word is None or category_id is None:
        return bad_request(None)
    else:
        category = model.get_list(category_id)
        if not category:
            return not_found(None)
        
        return create_card_json(word,category_id)

        
@api.route("/categories/<int:id>/cards/json",methods=["POST"])
@requires_auth('create:card')
def append_card_json(payload,id):
    category = model.get_list(id)
    word = request.json.get('word')
    if not category:
        return not_found(None)
    else:
        if not request.json or not word:
            return bad_request(None)
        
        return create_card_json(word,id)
    
    
@api.route('/cards/<int:id>/json', methods=['DELETE'])
@requires_auth('delete:card')
def delete_cards_json(payload,id):
    data = model.delete_card(id)
    
    if data is None:
        return not_found(None)
    else:
        return jsonify({'success':True,'message': 'card deleted'}),204
    
@api.route('/categories/<int:id>/json', methods=['DELETE'])
@requires_auth('delete:category')
def delete_categories_json(payload,id):
    error = model.delete_list(id)
    
    if error:
        return not_found(None)
    else:
        return jsonify({'success':True,'message': 'category deleted'}),204
    