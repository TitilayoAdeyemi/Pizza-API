from flask import Flask
from .orders.views import order_namespace
from .auth.views import auth_namespace
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.orders import Orders
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):

    
    
    app = Flask(__name__)

    app.config.from_object(config)

    authorizations= {
    'Bearer Auth' : {
    'type' : 'apiKey',
    'in' : 'header',
    'name' : 'Authorization',
    'description' : 'Add a JWT with ** Bearer &lt;JWT&gt; to authorize'
    }
            }

    api = Api(app,
               title='A Pizza delivery API',
                authorizations=authorizations,
                description= 'An API for a Pizza delivery service using Flask restx',
                security= 'Bearer Auth'
                )


    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error' : 'Not Found'}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_alowed(error):
        return {'error' : 'Method not allowed'}, 405

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace, path='/auth')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order' : Orders
        }

    return app
