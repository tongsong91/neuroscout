from marshmallow import Schema, fields
import webargs as wa
from flask_apispec import MethodResource, marshal_with, use_kwargs, doc
from models import Predictor, PredictorEvent
from . import utils

class PredictorSchema(Schema):
	id = fields.Int()
	name = fields.Str(description="Predictor name.")
	description = fields.Str()
	ef_id = fields.Int(description="Original extracted feature id.")

class PredictorSingleSchema(PredictorSchema):
	run_statistics = fields.Nested('PredictorRunSchema', many=True)

class PredictorEventSchema(Schema):
	id = fields.Str()
	onset = fields.Number(description="Onset in seconds.")
	duration = fields.Number(description="Duration in seconds.")
	value = fields.Number(description="Value, or amplitude.")
	run_id = fields.Int()
	predictor_id = fields.Int()

class PredictorRunSchema(Schema):
	run_id = fields.Int()
	mean = fields.Number()
	stdev = fields.Number()

class PredictorResource(MethodResource):
	@doc(tags=['predictors'], summary='Get predictor by id.')
	@marshal_with(PredictorSingleSchema)
	def get(self, predictor_id, **kwargs):
		return utils.first_or_404(Predictor.query.filter_by(id=predictor_id))

class PredictorListResource(MethodResource):
	@doc(tags=['predictors'], summary='Get list of predictors.',)
	@marshal_with(PredictorSchema(many=True))
	@use_kwargs({
	    'run_id': wa.fields.DelimitedList(fields.Int(),
	                                      description="Run id(s)"),
	    'name': wa.fields.DelimitedList(fields.Str(),
	                                    description="Predictor name(s)"),	}, locations=['query'])
	def get(self, **kwargs):
		# Get Predictors that match up to specified runs
		if 'run_id' in kwargs:
			run_id = kwargs.pop('run_id')
			kwargs['id'] = PredictorEvent.query.filter(
				PredictorEvent.run_id.in_(run_id)).distinct(
					'predictor_id').with_entities('predictor_id').all()

		query = Predictor.query
		for param in kwargs:
			query = query.filter(getattr(Predictor, param).in_(kwargs[param]))

		return query.all()

class PredictorEventListResource(MethodResource):
	@doc(tags=['predictors'], summary='Get events for predictor(s)',)
	@marshal_with(PredictorEventSchema(many=True))
	@use_kwargs({
	    'run_id': wa.fields.DelimitedList(fields.Int(),
	                                      description="Run id(s)"),
	    'predictor_id': wa.fields.DelimitedList(fields.Int(),
	                                    description="Predictor id(s)"),
	}, locations=['query'])
	def get(self, **kwargs):
		query = PredictorEvent.query
		for param in kwargs:
			query = query.filter(getattr(PredictorEvent, param).in_(kwargs[param]))
		return query.all()
