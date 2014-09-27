from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class Spiff(restful.Resource):
    def get(self):
        return {'version': '0.0.1'}

api.add_resource(Spiff, '/v1/spiff')

if __name__ == '__main__':
  app.run(debug=True)
