from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GradeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String(10))
    semester=db.Column(db.Integer)
    subject=db.Column(db.String(10))
    _40_49 = db.Column(db.Float, nullable=True)
    _50_59 = db.Column(db.Float, nullable=True)
    above_60 = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)

class KtReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String(10))
    semester=db.Column(db.Integer)
    appeared = db.Column(db.Integer)
    failed = db.Column(db.Integer)
    all_clear = db.Column(db.Integer)
    kt1 = db.Column(db.Integer)
    kt2 = db.Column(db.Integer)
    kt3 = db.Column(db.Integer)
    kt4 = db.Column(db.Integer)
    kt5 = db.Column(db.Integer)
