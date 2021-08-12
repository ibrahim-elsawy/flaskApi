from flask_restful import Api, Resource
from utils.process import get_response
from flask import Flask, flash, request, redirect, url_for


app = Flask(__name__)
api = Api(app)

class Process(Resource):
	def post(self):
		req = request.get_json()
		# return get_response(req['text'])
		try:
			return {"data":get_response(req['data'])}
		except Exception as e:
			return {"data": "Sorry we out of service right now for developing"}
		# return {"data" : req['data']}


api.add_resource(Process, "/process")
if __name__ == "__main__":
	app.run(debug=True)