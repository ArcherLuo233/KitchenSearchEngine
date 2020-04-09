from app import db

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    keyword = db.Column(db.String(1000), unique=False, nullable=False)
    time= db.Column(db.DateTime, unique=False, nullable=False)
