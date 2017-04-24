from flask_restful import Resource, abort
from flask_restful_swagger.swagger import operation
from flask_jwt import jwt_required
from marshmallow import Schema, fields
from models.stimulus import Stimulus

class StimulusSchema(Schema):
	id = fields.Str(dump_only=True)

	class Meta:
		additional = ('name', 'mimetype', 'path')

class StimulusResource(Resource):
	""" A stimulus """
	@operation()
	@jwt_required()
	def get(self, stimulus_id):
		""" Acess a specific stimulus """
		result = Stimulus.query.filter_by(id=stimulus_id).first_or_404()
		return StimulusSchema().dump(result)
