from database import db

class ExtractedFeature(db.Model):
	""" Events extracted from a Stimulus using an Extractor"""
	__table_args__ = (
	    db.UniqueConstraint('extractor_name', 'extractor_parameters', 'feature_name'),
	)

	id = db.Column(db.Integer, primary_key=True)
	# Hash of next three variables
	sha1_hash = db.Column(db.Text, nullable=False, unique=True)
	extractor_name = db.Column(db.String)
	extractor_parameters = db.Column(db.Text)
	feature_name = db.Column(db.String)

	extracted_events = db.relationship('ExtractedEvent', backref='extracted_feature',
                                		lazy='dynamic')
	generated_predictors = db.relationship('Predictor',
											backref='extracted_feature')


class ExtractedEvent(db.Model):
	""" Events extracted from a Stimuli"""
	id = db.Column(db.Integer, primary_key=True)
	onset = db.Column(db.Float)
	duration = db.Column(db.Float)
	value = db.Column(db.Float, nullable=False)
	history = db.Column(db.String)

	stimulus_id = db.Column(db.Integer, db.ForeignKey('stimulus.id'), nullable=False)
	ef_id = db.Column(db.Integer, db.ForeignKey(ExtractedFeature.id),
						   nullable=False)
