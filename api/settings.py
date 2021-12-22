import os

schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'firstname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 10,
    }
}

DOMAIN = {'people': {'schema': schema}}
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

MONGO_HOST = 'mongo'
MONGO_PORT = 27017

# Skip this block if your db has no auth. But it really should.
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_AUTH_SOURCE = 'admin'
MONGO_DBNAME = 'people'

