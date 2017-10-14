from flask import Flask, jsonify, request

from flask_swaggervalidator import decorators


app = Flask(__name__)


@app.route('/')
@decorators.validate_swagger_request('api.say_hello')
@decorators.validate_swagger_response('api.say_hello')
def say_hello():
    name = request.args.get('name', 'Unknown')
    data = {
        'weekend_greeting': 'Welcome to the weekend, {}!'.format(name),
        'pizza_party': 1
    }
    return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
