import unittest
import json

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import sys
import os
from flask import Flask,url_for

sys.path.append('../')

import config
from flashcard import create_app,model
from flashcard.api import api_crud


basedir = os.path.abspath(os.path.dirname(__file__))

class ClientTestCase(unittest.TestCase): 

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.homepage_endpoint = url_for('api.view_json')
        self.category_endpoint = lambda category_id:  url_for('get_category',id=category_id)
        self.cards_endpoint = lambda category_id:  url_for('append_card_json',id=category_id)
        self.card_endpoint = lambda card_id:  url_for('view_card_json',id=card_id)
        self.post_card_endpoint = url_for('api.create_cards_json')

        
        
    def test_home_page(self):
        """Test _____________ """
        res = self.client().get('/api/v1/json')
        self.assertEqual(res.status_code, 200)
        
    def tearDown(self):
        """Executed after reach test"""
        self.app_context.pop()
        
        
        
class APITestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.homepage_endpoint = url_for('api.view_json')
        self.category_endpoint = lambda category_id:  url_for('get_category',id=category_id)
        self.cards_endpoint = lambda category_id:  url_for('append_card_json',id=category_id)
        self.card_endpoint = lambda card_id:  url_for('view_card_json',id=card_id)
        self.post_card_endpoint = url_for('api.create_cards_json')

        
    def tearDown(self):
        """Executed after reach test"""
        self.app_context.pop()
        
    def delete_category(self,name):
        id = model.get_id(name)
        if id:
            error = model.delete_list(id)
            print('delete_category',error)
            
    def delete_card(self,word):
        id = model.get_card_id(word)
        if id:
            error = model.delete_card(id)
        
        
    def add_category(self,name,code):
        data = {}
        data['name'] = name
        data['code'] = code
        id = model.get_id(name)
        
        if id is None:
            error,_= model.create_list(data)
        
    def test_category_get(self):
        """Test _____________ """
        name = "English -> French"
        code = "en->fr"
        
        # delete category if it exists
        self.delete_category(name)   
        
        self.add_category(name,code)
        res = self.client().get(self.category_endpoint(model.get_id(name)))
        self.assertEqual(res.status_code, 200)
        
        
    def test_category_deletion(self):
        """Test _____________ """
        name = "English -> French"
        code = "en->fr"
        
        self.add_category(name,code)
        category_id = model.get_id(name)
        res = self.client().delete(self.category_endpoint(category_id))
        self.assertEqual(res.status_code, 204)
        res = self.client().get(self.category_endpoint(category_id))
        self.assertEqual(res.status_code, 404)
        
    def test_card_deletion(self):
        name = "English -> French"
        code = "en->fr"
        
        self.add_category(name,code)
        res = self.client().post(self.post_card_endpoint, data=json.dumps({'word':'hello','category_id':model.get_id(name)}), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().delete(self.card_endpoint(res.json['card'].get('id')))
        self.assertEqual(res.status_code,204)
        
        
    def test_posts(self):
        # delete english->japanese category if it exists
        self.delete_category('English -> Japanese')
        
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'Japanese'}), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        id = res.json['id']
        endpoint = res.json['cards_url']
        res = self.client().post(self.endpoint, data=json.dumps({'word':'hello'}), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        # try posting the same category again
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'Japanese'}), content_type='application/json')
        self.assertEqual(res.status_code, 409)
        

if __name__ == '__main__':
    unittest.main()