import logging
import re
from flask import current_app, Flask, jsonify, redirect, url_for, render_template,Blueprint,session,flash,request
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from flashcard.auth.authentication import requires_login,verify_decode_jwt
from .main import main_crud
from .api import api_crud
from .forms import ApiForm
import sys

sys.path.append('../')
from config import Config
from authlib.integrations.flask_client import OAuth

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv(sys.path[1]))


'helper function'
def get_uri(form):
    uri_map = {}
    uri_map[('DELETE','category')] = url_for('api.delete_categories_json',id=form.category_id.data)
    uri_map[('DELETE','card')] = url_for('api.delete_cards_json',id=form.card_id.data)
    uri_map[('GET','categories')] = url_for('api.list_json')
    uri_map[('GET','category')] = url_for('api.get_category',id=form.category_id.data)
    uri_map[('GET','cards')] = url_for('api.view_json',id=form.category_id.data)
    uri_map[('GET','card')] = url_for('api.view_card_json',id=form.card_id.data)
    uri_map[('POST','categories')] = url_for('api.create_categories_json')
    uri_map[('POST','card from category')] = url_for('api.append_card_json',id=form.category_id.data)
    uri_map[('POST','card')] = url_for('api.create_cards_json')
    
    return uri_map.get((form.method.data,form.resource.data))
    
    

def create_app(config=Config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'rabb911ay'
    print(config.AUTH0_DOMAIN)
    app.debug = debug
    app.testing = testing
    Bootstrap(app)
    oauth = OAuth(app)
    oauth.register(
        "auth0",
        client_id=Config.AUTH0_CLIENTID,
        client_secret=Config.AUTH0_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{Config.AUTH0_DOMAIN}/.well-known/openid-configuration',
    )
    
    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():        
        from . import model
        model.init_app(app)
        model._create_database()
        CORS(app)


    # Register blueprints.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/flashcards')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

        
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE'
        )
        return response
   

    # add default routes    
    @app.route("/contact.html")
    @requires_login()
    def contact():
        return render_template("contact.html")
    
    @app.route("/test_api",methods=['GET','POST'])
    @requires_login()
    def api_test():
        form = ApiForm()
        
        if request.method == "GET":
            return render_template("api.html",form=form)
        
        else:
            if form.validate_on_submit():
                print('apiform validated')
                uri = get_uri(form)
            
                if not uri:
                    flash("This combination of method and resource is not supported, please submit a valid input!")
                    return render_template('api.html',form=form,id_token=session['id_token'])
                
                curl_string = '''curl -X {} http://127.0.0.1:5555{} -H "Content-Type:application/json" -H "Authorization: Bearer {}"
                        '''.format(form.method.data,uri,session['id_token'])
            
                if form.method.data == 'POST':
                    if form.resource.data == 'categories':
                        if form.source is None or form.target is None:
                            flash('source or target is missing')
                            return render_template('api.html',form=form,id_token=session['id_token'])
                        
                        json = {"source":form.source.data,"target":form.target.data}            
                    else:
                        if form.word is None or form.category_id is None:
                            flash('word or category_id is missing')
                            return render_template('api.html',form=form,id_token=session['id_token'])
                        
                        json = {"word":form.word.data,"category_id":form.category_id.data}
                    
                    
                    curl_string += " -d '{json}'"
                    
                    
                return render_template('api.html',form=form,id_token=session['id_token'],curl_string=curl_string)
        
            else:
                print('not validated')
                print(form.errors.items())
                return render_template('api.html',form=form,id_token=session['id_token'])
            
    
    
    @app.route("/")
    def index():
        return render_template('login.html')
        
    @app.route('/login')
    def login():
        redirect_uri = url_for('callback', _external=True)
        return oauth.auth0.authorize_redirect(redirect_uri)

    @app.route('/callback')
    def callback():
        token = oauth.auth0.authorize_access_token()
         # do something with the token
         
        session['sub'] = token.get('userinfo').get('sub')
        session['id_token'] = token.get('id_token')
        print(session)
        return redirect(url_for('main.list'))
    

    @app.route('/logout')
    @requires_login()
    def logout():
        session.clear()
        client_id = Config.AUTH0_CLIENTID
        domain = Config.AUTH0_DOMAIN
        return_to = 'http://127.0.0.1:5555/'
        return redirect(
            f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}',
            code=302,
        )
    
    

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app