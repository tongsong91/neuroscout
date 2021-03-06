from marshmallow import Schema, fields
from flask_apispec import MethodResource, marshal_with, doc
from models import Stimulus
from . import utils

class StimulusSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    mimetype = fields.Str(dump_only=True, description='modality/mimetype')

class StimulusResource(MethodResource):
    @doc(tags=['stimulus'], summary='Get stimulus by id.')
    @marshal_with(StimulusSchema)
    def get(self, stimulus_id):
        return utils.first_or_404(Stimulus.query.filter_by(id=stimulus_id))
