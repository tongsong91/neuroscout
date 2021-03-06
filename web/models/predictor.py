from database import db
from sqlalchemy.ext.hybrid import hybrid_property
import statistics

class Predictor(db.Model):
	""" Instantiation of a predictor in a dataset.
		A collection of PredictorEvents. """
	__table_args__ = (
		db.UniqueConstraint('name', 'dataset_id'),
	)
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	description = db.Column(db.Text) # Where to get this from?

	dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
	ef_id = db.Column(db.Integer, db.ForeignKey('extracted_feature.id'))

	predictor_events = db.relationship('PredictorEvent', backref='predictor',
								lazy='dynamic')

	run_statistics = db.relationship('PredictorRun')

class PredictorEvent(db.Model):
	""" An event within a Predictor. Onset is relative to run. """
	__table_args__ = (
	    db.UniqueConstraint('onset', 'run_id', 'predictor_id'),
	)
	id = db.Column(db.Integer, primary_key=True)

	onset = db.Column(db.Float, nullable=False)
	duration = db.Column(db.Float)
	value = db.Column(db.String, nullable=False)

	run_id = db.Column(db.Integer, db.ForeignKey('run.id'), nullable=False)
	predictor_id = db.Column(db.Integer, db.ForeignKey('predictor.id'),
							nullable=False)

class PredictorRun(db.Model):
	""" Predictor run association cache table """
	run_id = db.Column(db.Integer, db.ForeignKey('run.id'), primary_key=True)
	predictor_id = db.Column(db.Integer, db.ForeignKey('predictor.id'), primary_key=True)

	def stat_property(function):
		@property
		def wrapper(self):
			val_query = PredictorEvent.query.filter_by(
					run_id=self.run_id,
					predictor_id=self.predictor_id).with_entities('value')
			try:
				return function(self, [float(a[0]) for a in val_query])
			except ValueError:
				return None
		return wrapper

	@stat_property
	def mean(self, values):
		return statistics.mean(values)

	@stat_property
	def stdev(self, values):
		return statistics.stdev(values)
