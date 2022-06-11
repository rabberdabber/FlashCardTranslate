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

token = None
subject = None
class ClientTestCase(unittest.TestCase): 

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app_context:
            self.homepage_endpoint = url_for('api.get_categories')
    
        
    def tearDown(self):
        """Executed after reach test"""
        self.app_context.pop()
    
    def get_api_headers(self):  
        return {
            'Authorization':
                'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }   
        
    def test_home_page(self):
        """Test _____________ """
        res = self.client().get(self.homepage_endpoint,headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200) 
        
  
class APITestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app_context:
            self.homepage_endpoint = url_for('api.get_categories')
            self.category_endpoint = lambda category_id:  url_for('api.get_category',id=category_id)
            self.cards_endpoint = lambda category_id:  url_for('api.get_cards',id=category_id)
            self.card_endpoint = lambda card_id:  url_for('api.get_card',id=card_id)
            self.post_card_endpoint = url_for('api.post_card')
            self.post_category_endpoint = url_for('api.post_category')
            self.post_card_from_category_endpoint = lambda category_id: url_for('api.post_card_from_category',id=category_id)
            self.delete_card_endpoint = lambda card_id: url_for('api.delete_card',id=card_id)
            self.delte_category_endpoint = lambda category_id: url_for('api.delelte_category',id=category_id)

        
    def tearDown(self):
        """Executed after reach test"""
        self.app_context.pop()
        
    def get_api_headers(self):  
        return {
            'Authorization':
                'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        
    def test_category_get(self):
        """Test _____________ """
       
        # add English->French category if it doesn't exist then get it
        res = self.client().post(self.post_category_endpoint, data=json.dumps({'source':'English','target':'French'}),headers=self.get_api_headers())
        res = self.client().get(self.category_endpoint(res.json['id']),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200)
        
        
    def test_category_deletion(self):
        """Test _____________ """
        name = "English -> French"
        code = "en->fr"
        
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'French'}),headers=self.get_api_headers())
        category_id = res.json['id']
        res = self.client().delete(self.category_endpoint(category_id),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 204)
        res = self.client().get(self.category_endpoint(category_id),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 404)
        
    def test_card_deletion(self):
        name = "English -> French"
        code = "en->fr"
        
        # add English to French category if it doesn't exist
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'French'}),headers=self.get_api_headers())
       
        id = res.json['id']
        res = self.client().post(self.post_card_endpoint, data=json.dumps({'word':'hello','category_id':id}),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 201)
        res = self.client().delete(self.card_endpoint(res.json['card'].get('id')),headers=self.get_api_headers())
        self.assertEqual(res.status_code,204)
        
        
    def test_posts(self):
        # delete english->japanese category if it exists
        
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'Japanese'}),headers=self.get_api_headers())
        if res.status_code == 409:
            res = self.client().delete(self.card_endpoint(res.get('id')),headers=self.get_api_headers())
            self.assertEqual(res.status_code,204)
        
        # test posts 
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'Japanese'}),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 201)
        id = res.json['id']
        endpoint = res.json['cards_url']
        res = self.client().post(self.endpoint, data=json.dumps({'word':'hello'}), headers=self.get_api_headers())
        self.assertEqual(res.status_code, 201)
        # try posting the same category again
        res = self.client().post(self.homepage_endpoint, data=json.dumps({'source':'English','target':'Japanese'}),headers=self.get_api_headers())
        self.assertEqual(res.status_code, 409)
        

if __name__ == '__main__':
    unittest.main()